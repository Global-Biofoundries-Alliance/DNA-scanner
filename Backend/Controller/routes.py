from flask import request, json
from flask import session as flaskSession

from .app import app
from Pinger.Pinger import *

from .service import DefaultComparisonService as Service
from .configurator import YmlConfigurator as Configurator
from .session import InMemorySessionManager as SessionManager

# TODO Set string to point on Yml file
# TODO Set SessionId
# TODO use service in endpoints
service = Service(Configurator("config.yml"), SessionManager("Meine SessionId"))

#
#   Provides clients with a complete list of vendors available
#
@app.route('/vendors', methods=['get'])
def get_vendors():
    return json.jsonify(service.getVendors())


@app.route('/ping')
def hello_world():
    return 'pong'


@app.route('/upload', methods=['post'])
def uploadFile():
    if 'seqfile' not in request.files or request.files['seqfile'] == "":
        return json.jsonify({'error': 'No file specified'})

    return service.setSequencesFromFile(request.files["seqfile"])


@app.route('/filter', methods=['POST'])
def filterResults():
    if not request.is_json:
        return {'error': 'Invalid filter request: Data must be in JSON format'}

    request_json = request.get_json()
    if 'filter' not in request_json:
        return {'error': 'Request is missing filter attribute'}

    # check if all keys are in the request
    if any(key not in request_json['filter'] for key in
           {'vendors', 'price', 'deliveryDays', \
            'preselectByPrice', 'preselectByDeliveryDays'}):
        return {'error': 'Malformed filter'}

    service.setFilter(request_json["filter"])

    return 'filter submission successful'


@app.route('/results', methods=['POST'])
def getSearchResults():
    # Get size and offset fields if available and set them to default otherwise
    size = 1000
    offset = 0
    if request.form.get('size'):
        size = int(request.form.get('size'))
    if request.form.get('offset'):
        offset = int(request.form.get('offset'))

    return service.getResults(size=size, offset=offset)
