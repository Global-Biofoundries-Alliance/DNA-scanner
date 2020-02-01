import tempfile
from random import random, randint

from flask import request, json, session
from werkzeug.utils import secure_filename

from .app import app
from .transformation import buildSearchResponseJSON, sequenceInfoFromObjects, filterOffers
from .dataformats import Filter
from .parser import parse
from Pinger.Pinger import *
from Pinger.AdvancedMock import AdvancedMockPinger
from Pinger.GeneArt import GeneArt

from .service import DefaultComparisonService as Service
from .configurator import YmlConfigurator as Configurator
from .session import InMemmorySessionManager as SessionManager

# TODO Set string to point on Yml file
# TODO Set SessionId
# TODO use service in endpoints
service = Service(Configurator("Path to Yaml Configuration"), SessionManager("Meine SessionId")) 

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

    except:
        return json.jsonify({'error': 'File format not supported'})

    return 'upload successful'


@app.route('/filter', methods=['POST'])
def filterResults():
    if not request.is_json:
        return {'error': 'Invalid filter request: Data must be in JSON format'}

    request_json = request.get_json()
    if 'filter' not in request_json:
        return {'error': 'Request is missing filter attribute'}

    # check if all keys are in the request
    if any(key not in request_json['filter'] for key in
           {'vendors', 'price', 'deliveryDays',\
            'preselectByPrice', 'preselectByDeliveryDays'}):
        return {'error': 'Malformed filter'}

    previousVendors = set()
    if 'filter' in session:
        previousVendors = set(session['filter']['vendors'])

    session['filter'] = request_json['filter']
    currentVendors = set(session['filter']['vendors'])

    for vendor in previousVendors - currentVendors:
        pass  # TODO: Remove filtered out vendor pingers

    for vendor in currentVendors - previousVendors:
        pass  # TODO: Add newly added vendor pingers

    return 'filter submission successful'


@app.route('/results', methods=['POST'])
def getSearchResults():
    if 'sequences' not in session:
        return {'error': 'No sequences available'}

    mainPinger = CompositePinger()
    # Begin temporary testing placeholders
    for id in range(0, len(vendors)):
        dummyVendor = VendorInformation(vendors[id]["name"], vendors[id]["shortName"], id)
        if id == 2:
            # TODO Init Geneart-Pinger by config
            pinger = GeneArt(username = 'username', token = 'token')
            mainPinger.registerVendor(dummyVendor, pinger)
        else:
            mainPinger.registerVendor(dummyVendor, AdvancedMockPinger(dummyVendor))
    # End temporary testing placeholders

    sequences = []
    for seq in session['sequences']:
        sequences.append(SequenceInformation(key=seq["key"], name=seq["name"], sequence=seq["sequence"]))

    # Search and retrieve offers for each sequence
    mainPinger.searchOffers(sequences)
    seqoffers = mainPinger.getOffers()

    # Get size and offset fields if available and set them to default otherwise
    size = len(sequences)
    offset = 0
    if request.form.get('size'):
        size = int(request.form.get('size'))
    if request.form.get('offset'):
        offset = int(request.form.get('offset'))

    # build response from offers stored in the session
    if "filter" in session:
        result = buildSearchResponseJSON(filterOffers(session["filter"], seqoffers), vendors, offset, size)
    else:
        result = buildSearchResponseJSON(seqoffers, vendors, offset, size)

    return result

