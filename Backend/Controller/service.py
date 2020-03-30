from sys import maxsize

import os
import tempfile
from Pinger.Entities import *
from Pinger.Entities import VendorInformation, SequenceInformation
from Pinger.Pinger import *
from Pinger.Validator import EntityValidator
from flask import json
from flask import session as session_cookie
from secrets import token_urlsafe
from typing import List
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .parser import parse, BoostClient
from .session import InMemorySessionManager as SessionManager
from .transformation import buildSearchResponseJSON, sequenceInfoFromObjects, filterOffers

# This doesn't actually hold state so it can be global
validator = EntityValidator()


#
#   Abstract representation of a service containing the central functionality of the application.
#   It should only ever contain functionality but not state.
#   For state it holds a Configurator object for static information obtained via global configuration
#   and a SessionManager object which holds session specific information between calls.
#
#   Note that not every method here has to correspond to exactly one end point.
#   Some methods might be useful for more than one end point while some may only be part of an endpoint
#   but deserves its own method for atomicity reasons
#
class ComparisonService:

    def __init__(self, configurator):
        raise NotImplementedError

    #
    #   Receives a werkzeug FileStorage, extracts sequences from it and stores them in the session
    #
    def setSequencesFromFile(self, seqfile: FileStorage, prefix: str) -> None:
        raise NotImplementedError

    #
    #   Directly stores a list of sequences in the session
    #
    def setSequences(self, sequences: List[SequenceInformation]) -> None:
        raise NotImplementedError

    #
    #   Sets the filter settings
    #
    def setFilter(self, filter: dict) -> None:
        raise NotImplementedError

    #
    #   Returns all search results packed into a JSON response
    #
    def getResults(self, size: int, offset: int):
        raise NotImplementedError

    #
    #   Returns the list of available vendors
    #
    def getVendors(self) -> List[VendorInformation]:
        raise NotImplementedError

    #
    #   Returns a list of available host organisms
    #
    def getAvailableHosts(self):
        raise NotImplementedError

    def setCodonOptimizationOptions(self, host, strategy):
        raise NotImplementedError


class DefaultComparisonService(ComparisonService):

    def __init__(self, configurator):
        self.config = configurator

    #
    # Parses an uploaded sequence file and stores the sequences in the session
    #
    def setSequencesFromFile(self, seqfile: FileStorage, prefix: str):
        # Store the input in a temporary file for the parser to process
        tempf, tpath = tempfile.mkstemp(
            '.' + secure_filename(seqfile.filename).rsplit('.', 1)[1].lower())
        seqfile.save(tpath)
        seqfile.close()

        objSequences = []
        try:
            session = self.getSession()
            isProtein = session.loadHostOrganism() != ""
            # Parse sequence file
            objSequences = parse(tpath, isProtein, self.getBoostClient(), session.loadHostOrganism(),
                                 session.loadJugglingStrategy())
        except Exception as e:
            print(e)
            return json.jsonify({'error': 'File format not supported'})

        finally:
            # Cleanup
            os.close(tempf)
            os.remove(tpath)

        # Convert [SeqObject] to [SequenceInformation]
        sequences = sequenceInfoFromObjects(objSequences)
        # Add specified prefix
        for seq in sequences:
            uniqueID = str(SequenceInformation.generateId())
            seq.name = uniqueID + "_" + prefix + "_" + seq.name
            seq.key = uniqueID

        self.setSequences(sequences)

        return 'upload successful'

    #
    # Stores an explicit list of sequences in the session
    #
    def setSequences(self, sequences: List[SequenceInformation]):
        session = self.getSession()

        # Input check
        realSequences = []
        for seq in sequences:
            if not isinstance(seq, SequenceInformation):
                print("Invalid input in DefaultComparisonService.setSequences: Type is not SequenceInformation.")
                continue
            if not validator.validate(seq):
                continue
            realSequences.append(seq)

        session.storeSequences(realSequences)

        # Prepare template offer list
        seqoffers = []
        for seq in realSequences:
            seqoff = SequenceVendorOffers(seq, [])
            for vendor in self.config.vendors:
                seqoff.vendorOffers.append(VendorOffers(vendor, []))
            seqoffers.append(seqoff)

        # Clear results and state concerning them
        session.storeResults(seqoffers)
        session.resetSearchedVendors()
        session.storeSelection([])

    #
    # Sets the filter settings
    #
    def setFilter(self, filter: dict):
        session = self.getSession()
        session.storeFilter(filter)
        session.storeSelection([])

    #
    # Sets which sequences are marked as selected
    #
    def setSelection(self, selection: List[List]):
        self.getSession().storeSelection(selection)

    #
    #   Returns all search results packed into a JSON response
    #
    def getResults(self, size: int, offset: int):
        session = self.getSession()

        if not session.loadSequences():
            return {'error': 'No sequences available'}

        sequences = session.loadSequences()
        seqoffers = session.loadResults()

        filter = session.loadFilter()

        # Create a list of vendors to contact in the search process.
        # Only vendors that are to be searched by the filter settings
        # and that have not been contacted yet are to be contacted.
        # This is for saving network overhead on both sides.
        vendorsToSearch = []
        if "vendors" in filter:
            # Only contact vendors that are allowed in the filter
            for key in filter["vendors"]:
                if key not in session.loadSearchedVendors():
                    vendorsToSearch.append(key)
        else:
            # If there are no vendor preferences just contact all
            for vendor in self.config.vendors:
                if vendor.key not in session.loadSearchedVendors():
                    vendorsToSearch.append(vendor.key)

        # Only do a search if any vendors are to be contacted as everything else would be quite pointless
        if vendorsToSearch:
            mainPinger = session.loadPinger()
            mainPinger.searchOffers(seqInf=sequences, vendors=vendorsToSearch)
            # Wait for the pinger to finish the search
            while mainPinger.isRunning():
                pass
            newoffers = mainPinger.getOffers()

            session.addSearchedVendors(vendorsToSearch)
            # TODO optimize the hell out of this
            for seqoff in seqoffers:
                for newseqoff in newoffers:
                    if seqoff.sequenceInformation.key == newseqoff.sequenceInformation.key:
                        for vendoff in seqoff.vendorOffers:
                            if vendoff.vendorInformation.key not in vendorsToSearch:
                                continue
                            for newvendoff in newseqoff.vendorOffers:
                                if vendoff.vendorInformation.key == newvendoff.vendorInformation.key:
                                    vendoff.offers.extend(newvendoff.offers)
                                    vendoff.messages.extend(newvendoff.messages)

            session.storeResults(seqoffers)

        # build response from offers stored in the session
        if not filter or filter["preselectByPrice"] or filter["preselectByDeliveryDays"]:

            # selection criterion; Default is selection by price
            # The '% maxsize's are there to ensure that negative numbers wrap around to
            # very high numbers, making them inferior to offers that provide this information
            # If the offer contains an error message it is to be treated as inferior as well.
            selector = (lambda x: (((x["turnoverTime"] % maxsize) if not x["offerMessage"] else maxsize),
                                   (x["price"] % maxsize) if not x["offerMessage"] else maxsize)) \
                if "preselectByDeliveryDays" in filter and filter["preselectByDeliveryDays"] else \
                (lambda x: (((x["price"] % maxsize) if not x["offerMessage"] else maxsize),
                            ((x["turnoverTime"] % maxsize) if not x["offerMessage"] else maxsize)))
            # Preselection by lambda
            result = buildSearchResponseJSON(filterOffers(filter, seqoffers), self.config.vendors, selector,
                                             session.loadGlobalMessages(),
                                             offset, size)
        else:
            # Use selection list
            result = buildSearchResponseJSON(filterOffers(filter, seqoffers), self.config.vendors,
                                             session.loadSelection(), session.loadGlobalMessages(),
                                             offset, size)

        return result

    #
    #   Returns the list of available vendors
    #
    def getVendors(self):
        return self.config.vendors

    #
    #   Returns a list of available host organisms
    #
    def getAvailableHosts(self):
        boost = self.getBoostClient()
        return boost.getPreDefinedHosts()

    #
    #   Sets the host organism and juggling strategy to be used in subsequent codon optimizations
    #
    def setCodonOptimizationOptions(self, host, strategy):
        session = self.getSession()
        session.storeHostOrganism(host)
        session.storeJugglingStrategy(strategy)

    #
    #   Orders a list of offer ids
    #
    #   @param offer_ids A list of offer ids to order
    #
    def issueOrder(self, offer_ids):
        session = self.getSession()

        pinger = self.getSession().loadPinger()

        seqoffers = session.loadResults()
        offersPerVendor = [[] for v in self.config.vendors]

        for seqoffer in seqoffers:
            for vendoffer in seqoffer.vendorOffers:
                for offer in vendoffer.offers:
                    if offer.key in offer_ids:
                        offersPerVendor[vendoffer.vendorInformation.key].append(offer.key)

        orders = []
        for vendor in self.config.vendors:
            order = pinger.order(offersPerVendor[vendor.key], vendor.key)
            order_dict = order.__dict__()
            order_dict["vendor"] = vendor.key
            orders.append(order_dict)

        return orders

    #
    #   Returns the current session or creates it if it hasn't been already.
    #
    def getSession(self) -> SessionManager:
        # Store a session identifier in the client-side cookie if not already present.
        # This is used to identify the server-side session later on.
        if "sessionKey" not in session_cookie:
            token = token_urlsafe(64)
            # Session collision prevention
            # (yes it's still random guessing but with that range it should not need many tries)
            while SessionManager.hasSession(token):
                token = token_urlsafe(64)
            session_cookie["sessionKey"] = token
        session = SessionManager(session_cookie["sessionKey"])

        if not session.loadPinger():  # This indicates that the session is new
            session.storePinger(self.config.initializePinger(session))
        return session

    #
    #   Returns the current session's BOOST client and configures it if nonexistent
    #
    def getBoostClient(self) -> BoostClient:
        session = self.getSession()
        boost = session.loadBoostClient()
        if not boost:
            boost = self.config.initializeBoostClient()
            boost.login()
            session.storeBoostClient(boost)
        return boost
