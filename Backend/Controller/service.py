import os
import tempfile
from typing import List

from Pinger.Entities import *
from Pinger.Entities import VendorInformation, SequenceInformation
from Pinger.Pinger import *
from Pinger.Validator import EntityValidator
from flask import json
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .parser import parse
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

    def __init__(self, configurator, sessionManager):
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

    def __init__(self, configurator, sessionManager):
        self.config = configurator
        self.session = sessionManager

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

        # Clear results
        self.session.storeResults([])

        return 'upload successful'

    #
    # Stores an explicit list of sequences in the session
    #
    def setSequences(self, sequences: List[SequenceInformation]):
        # Input check
        realSequences = []
        for seq in sequences:
            if not isinstance(seq, SequenceInformation):
                print("Invalid input in DefaultComparisionService.setSequences: Type is not SequenceInformation.")
                continue
            if not validator.validate(seq):
                continue
            realSequences.append(seq)

        self.session.storeSequences(sequences)

    #
    # Sets the filter settings
    #
    def setFilter(self, filter: dict):
        self.session.storeFilter(filter)

    #
    #   Returns all search results packed into a JSON response
    #
    def getResults(self, size: int, offset: int):
        if not self.session.loadSequences():
            return {'error': 'No sequences available'}

        sequences = self.session.loadSequences()
        seqoffers = self.session.loadResults()

        filter = self.session.loadFilter()

        #TODO implement lazy search
        if not seqoffers:
            vendorsToSearch = []
            for vendor in self.config.vendors:
                vendorsToSearch.append(vendor.key)

            mainPinger = self.config.pinger
            mainPinger.searchOffers(seqInf=sequences, vendors=vendorsToSearch)
            seqoffers = mainPinger.getOffers()

            self.session.storeResults(seqoffers)

        # build response from offers stored in the session
        result = buildSearchResponseJSON(filterOffers(self.session.loadFilter(), seqoffers), self.config.vendors,
                                         offset, size)

        return result

    #
    #   Returns the list of available vendors
    #
    def getVendors(self):
        return self.config.vendors
