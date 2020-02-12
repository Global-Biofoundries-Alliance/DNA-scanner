import os
import tempfile
from secrets import token_urlsafe
from typing import List

from Pinger.Entities import *
from Pinger.Entities import VendorInformation, SequenceInformation
from Pinger.Pinger import *
from Pinger.Validator import EntityValidator
from flask import json
from flask import session as session_cookie
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .parser import parse
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
    def setSequencesFromFile(self, seqfile: FileStorage) -> None:
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


class DefaultComparisonService(ComparisonService):

    def __init__(self, configurator):
        self.config = configurator

    #
    # Parses an uploaded sequence file and stores the sequences in the session
    #
    def setSequencesFromFile(self, seqfile: FileStorage):
        # Store the input in a temporary file for the parser to process
        tempf, tpath = tempfile.mkstemp(
            '.' + secure_filename(seqfile.filename).rsplit('.', 1)[1].lower())
        seqfile.save(tpath)

        try:
            # Parse sequence file
            objSequences = parse(tpath)

            # Convert [SeqObject] to [SequenceInformation] and store them in the session
            self.setSequences(sequenceInfoFromObjects(objSequences))

        except Exception as e:
            print(e)
            return json.jsonify({'error': 'File format not supported'})

        finally:
            # Cleanup
            os.remove(tpath)

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

        # Clear results
        session.storeResults(seqoffers)
        session.resetSearchedVendors()

    #
    # Sets the filter settings
    #
    def setFilter(self, filter: dict):
        session = self.getSession()
        session.storeFilter(filter)

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

        vendorsToSearch = []
        if "vendors" in filter:
            for key in filter["vendors"]:
                if key not in session.loadSearchedVendors():
                    vendorsToSearch.append(key)
        else:
            for vendor in self.config.vendors:
                if vendor.key not in session.loadSearchedVendors():
                    vendorsToSearch.append(vendor.key)

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
                                    vendoff.offers = newvendoff.offers


            session.storeResults(seqoffers)

        # selection criterion; Default is selection by price
        selector = \
            (lambda a, b: a if (a["turnoverTime"] < b["turnoverTime"]) \
                               or (a["turnoverTime"] == b["turnoverTime"] and a["price"] < b["price"]) \
                else b) \
                if "preselectByDeliveryDays" in filter and filter["preselectByDeliveryDays"] else \
                (lambda a, b: a if (a["price"] < b["price"]) \
                                   or (a["price"] == b["price"] and a["turnoverTime"] < b["turnoverTime"]) \
                    else b)

        # build response from offers stored in the session
        result = buildSearchResponseJSON(filterOffers(filter, seqoffers), self.config.vendors, selector,
                                         offset, size)

        return result

    #
    #   Returns the list of available vendors
    #
    def getVendors(self):
        return self.config.vendors

    #
    #   Returns the current session or creates it if it hasn't been already.
    #
    def getSession(self) -> SessionManager:
        if "sessionKey" not in session_cookie:
            session_cookie["sessionKey"] = token_urlsafe(64)
        session = SessionManager(session_cookie["sessionKey"])

        if not session.loadPinger():  # This indicates that the session is new
            session.storePinger(self.config.initializePinger())
        return session
