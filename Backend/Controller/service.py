# python imports
import os
import tempfile

from Pinger.AdvancedMock import AdvancedMockPinger
from Pinger.Entities import *
from Pinger.Pinger import *
# library imports
from flask import json, session
from werkzeug.utils import secure_filename

from .parser import parse
# project imports
from .transformation import buildSearchResponseJSON, sequenceInfoFromObjects, filterOffers

# All vendors known to the service
# TODO Incorporate this into the config and then remove this
vendors = [{"name": "TWIST DNA",
            "shortName": "TWIST",
            "key": 0},

           {"name": "IDT DNA",
            "shortName": "IDT",
            "key": 1},

           {"name": "GeneArt",
            "shortName": "GenArt",
            "key": 2}
           ]


#
#   Der ComparisonService ist das allgemeine Interface. Es geht darum hier Prozessfälle abzudecken,
#   welche die Funktionen des Vergleichs (Upload, Matrix, Filtern) ... abbildet.
#   Es muss nicht umbedingt für einen Endpunkt in routes eine Methode geben. Eventuell kann man
#   z.B. an einem Endpunkt 2 methoden verwenden, welche eventuell in anderen ENdpunkten auch 
#   verwendet werden.
#
#   Review könnte später z.B: in einem ReviewService umgesetzt werden.
#
#   Allgemeines Beispiel:
#       \setFilter -> changeFilter() 
#       \resultsByFilter -> changeFilter() -> getResults()
#

# TODO war jetzt noch nicht ganz durchdacht. wurde erstmal nur schnell hingeworfen.

class ComparisonService:

    def __init__(self, configurator, sessionManager):
        raise NotImplementedError

    def setSequencesFromFile(self, seqfile):
        raise NotImplementedError

    def setSequences(self, sequences):
        raise NotImplementedError

    def setFilter(self, filter):
        raise NotImplementedError

    def getVendors(self):
        raise NotImplementedError


# TODO implement
class DefaultComparisonService(ComparisonService):

    def __init__(self, configurator, sessionManager):
        self.config = configurator
        self.session = sessionManager

    # Parses an uploaded sequence file and stores the sequences in the session
    def setSequencesFromFile(self, seqfile):
        # Store the input in a temporary file for the parser to process
        tempf, tpath = tempfile.mkstemp(
            '.' + secure_filename(seqfile.filename).rsplit('.', 1)[1].lower())
        seqfile.save(tpath)

        try:
            # Parse sequence file
            objSequences = parse(tpath)

            # Convert [SeqObject] to [SequenceInformation] and store them in the session
            sequences = []
            for seqInfo in sequenceInfoFromObjects(objSequences):
                sequences.append({"key": seqInfo.key, "name": seqInfo.name, "sequence": seqInfo.sequence})

            self.setSequences(sequences)

        except Exception as e:
            print(e)
            return json.jsonify({'error': 'File format not supported'})

        finally:
            # Cleanup
            os.remove(tpath)

        return 'upload successful'

    # Stores an explicit list of sequences in the session (INPUT CHECK!!!)
    def setSequences(self, sequences):
        # TODO use session manager
        self.session.storeSequences(sequences)

    #
    def setFilter(self, filter):
        # TODO use session manager
        previousVendors = set()
        if 'filter' in session:
            previousVendors = set(session['filter']['vendors'])

        self.session.storeFilter(filter)
        currentVendors = set(filter['vendors'])

        for vendor in previousVendors - currentVendors:
            pass  # TODO: Remove filtered out vendor pingers

        for vendor in currentVendors - previousVendors:
            pass  # TODO: Add newly added vendor pingers

    def getResults(self, size, offset):
        if not self.session.loadSequences():
            return {'error': 'No sequences available'}

        #mainPinger = CompositePinger()
        # Begin temporary testing placeholders
        #for id in range(0, len(vendors)):
            #dummyVendor = VendorInformation(vendors[id]["name"], vendors[id]["shortName"], id)
            # if id == 2:
            #    # TODO Init Geneart-Pinger by config
            #    pinger = GeneArt(username='username', token='token')
            #    mainPinger.registerVendor(dummyVendor, pinger)
            # else:
            #mainPinger.registerVendor(dummyVendor, AdvancedMockPinger(dummyVendor))
        # End temporary testing placeholders

        mainPinger = self.config.pinger

        sequences = []
        for seq in self.session.loadSequences():
            sequences.append(SequenceInformation(key=seq["key"], name=seq["name"], sequence=seq["sequence"]))

        # Search and retrieve offers for each sequence
        mainPinger.searchOffers(sequences)
        seqoffers = mainPinger.getOffers()

        # build response from offers stored in the session
        result = buildSearchResponseJSON(filterOffers(self.session.loadFilter(), seqoffers), vendors, offset, size)
        #result = buildSearchResponseJSON(seqoffers, self.config.vendors, offset, size)

        return result

    def getVendors(self):
        return vendors
