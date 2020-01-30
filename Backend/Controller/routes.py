import tempfile
from random import random, randint

from flask import request, json, session
from werkzeug.utils import secure_filename

from .app import app
from .controllerutils import buildSearchResponseJSON, sequenceInfoFromObjects, filterOffers
from .dataformats import Filter
from .parser import parse
from Pinger.Pinger import *
from Pinger.AdvancedMock import AdvancedMockPinger

# All vendors known to the service
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
#   Provides clients with a complete list of vendors available
#
@app.route('/vendors', methods=['get'])
def get_vendors():
    return json.jsonify(vendors)


@app.route('/ping')
def hello_world():
    return 'pong'


@app.route('/upload', methods=['post'])
def uploadFile():
    if 'seqfile' not in request.files or request.files['seqfile'] == "":
        return json.jsonify({'error': 'No file specified'})

    # Store the input in a temporary file for the parser to process
    tempf, tpath = tempfile.mkstemp('.' + secure_filename(request.files['seqfile'].filename).rsplit('.', 1)[1].lower())
    request.files['seqfile'].save(tpath)

    try:
        # Parse sequence file
        objSequences = parse(tpath)

        # Convert [SeqObject] to [SequenceInformation] and store them in the session
        sequences = []
        for seqInfo in sequenceInfoFromObjects(objSequences):
            sequences.append({"key": seqInfo.key, "name": seqInfo.name, "sequence": seqInfo.sequence})
        session["sequences"] = sequences

    except NameError:
        return json.jsonify({'error': 'File format not supported'})

    return 'upload successful'


@app.route('/filter', methods=['POST'])
def filterResults():
    if not request.is_json:
        return {'error': 'Invalid filter request: Data must be in JSON format'}

    previousVendors = set()
    if 'filter' in session:
        previousVendors = set(session['filter']['vendors'])

    request_json = request.get_json()
    session['filter'] = request_json['filter']
    currentVendors = set(session['filter']['vendors'])

    for vendor in previousVendors - currentVendors:
        pass  # TODO: Remove filtered out vendor pingers

    for vendor in currentVendors - previousVendors:
        pass  # TODO: Add newly added vendor pingers

    return 'filter submission successful'


@app.route('/results', methods=['POST'])
def getSearchResults():

    return {
               "count": 5,
               "globalMessage": [],
               "offset": 0,
               "result": [
                   {
                       "sequenceInformation": {
                           "id": "B0012",
                           "length": 6,
                           "name": "Sequence 0",
                           "sequence": "ATTCGA"
                       },
                       "vendors": [
                           {
                               "key": 0,
                               "offers": []
                           },
                           {
                               "key": 1,
                               "offers": [
                                   {
                                       "offerMessage": [{"messageType": 1005, "text": "Sequence too long"}],
                                       "price": 0.0,
                                       "selected": False,
                                       "turnoverTime": 3
                                   },
                                   {
                                       "offerMessage": [],
                                       "price": 0.46,
                                       "selected": False,
                                       "turnoverTime": 4
                                   }
                               ]
                           },
                           {
                               "key": 2,
                               "offers": []
                           }
                       ]
                   },
                   {
                       "sequenceInformation": {
                           "id": "B0032",
                           "length": 11,
                           "name": "Sequence 1",
                           "sequence": "AATTATATAAA"
                       },
                       "vendors": [
                           {
                               "key": 0,
                               "offers": []
                           },
                           {
                               "key": 1,
                               "offers": [
                                   {
                                       "offerMessage": [],
                                       "price": 0.1,
                                       "selected": False,
                                       "turnoverTime": 1
                                   }
                               ]
                           },
                           {
                               "key": 2,
                               "offers": []
                           }
                       ]
                   }
               ],
               "size": 2
           }
