'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
import traceback

from flask import request, json

from Pinger.Pinger import *

from .app import app
from .configurator import YmlConfigurator as Configurator
from .service import DefaultComparisonService as Service


service = Service(Configurator("config.yml"))


#
#   Provides clients with a complete list of vendors available
#
@app.route('/vendors', methods=['get'])
def get_vendors():
    try:
        # Convert vendors into form used by frontend
        vendors = []
        for vendor in service.getVendors():
            vendors.append(
                {"name": vendor.name, "shortName": vendor.shortName, "key": vendor.key})
        return json.jsonify(vendors)
    except:
        return {"error": "Encountered error while getting vendors\n" + (traceback.format_exc() if __debug__ else "")}


#
#   Very simple endpoint to see if the service is up
#
@app.route('/ping')
def hello_world():
    return 'pong'


#
#   Upload a sequence file to this endpoint.
#   Currently supported formats are FASTA, GenBank and SBOL2.
#
@app.route('/upload', methods=['post'])
def uploadFile():
    try:
        # Input checking
        if 'seqfile' not in request.files or request.files['seqfile'] == "":
            return json.jsonify({'error': 'No file specified'})

        # Sequence prefix for this file's sequences
        seqPrefix = request.form.get("prefix", default="")

        # Actually parse the file and save the sequences
        return service.setSequencesFromFile(request.files["seqfile"], seqPrefix)
    except:
        return {"error": "Encountered error during file upload\n" + (traceback.format_exc() if __debug__ else "")}


#
#   Submit a filter as JSON here.
#   See documentation for filter format
#
@app.route('/filter', methods=['POST'])
def filterResults():
    try:
        # Check correct request format
        if not request.is_json:
            return {'error': 'Invalid filter request: Data must be in JSON format'}

        # Check if there is even a filter present
        request_json = request.get_json()
        if 'filter' not in request_json:
            return {'error': 'Request is missing filter attribute'}

        # Check if all keys are in the request
        if any(key not in request_json['filter'] for key in
               {'vendors', 'price', 'deliveryDays',
                'preselectByPrice', 'preselectByDeliveryDays'}):
            return {'error': 'Malformed filter'}

        # Store the filter
        service.setFilter(request_json["filter"])

        return 'filter submission successful'
    except:
        return {"error": "Encountered error setting filter\n" + (traceback.format_exc() if __debug__ else "")}


#
#   call this route to receive the results gathered.
#
#   parameters per form data:
#       size: The number of results to be shown (note that there might be less available
#       offset: The index of the offer to start at (starting at 0)
#
@app.route('/results', methods=['POST'])
def getSearchResults():
    try:
        # Get size and offset fields if available and set them to default
        # otherwise
        size = 10000000  # Nobody has plates this large
        offset = 0
        if request.form.get('size'):
            size = int(request.form.get('size'))
        if request.form.get('offset'):
            offset = int(request.form.get('offset'))

        # Get the results from the service
        return service.getResults(size=size, offset=offset)
    except Exception as error:
        return {"error": "Encountered error while fetching search results\n" + (
            traceback.format_exc() if __debug__ else "")}


@app.route('/select', methods=['POST'])
def setSelection():
    try:
        service.setSelection(request.get_json()["selection"])
        return 'selection set'
    except Exception as error:
        return {"error": "Encountered error while selecting offers\n" + (
            traceback.format_exc() if __debug__ else "")}


@app.route('/available_hosts', methods=['GET'])
def getAvailableHosts():
    try:
        return json.jsonify(service.getAvailableHosts())
    except Exception as error:
        return {"error": "Encountered error while fetching list of available hosts\n" + (
            traceback.format_exc() if __debug__ else "")}


@app.route('/codon_optimization', methods=['POST'])
def setCodonOptimizationOptions():
    try:
        request_json = request.get_json()
        if "strategy" not in request_json or "host" not in request_json:
            return {"error": "Request is missing fields"}

        service.setCodonOptimizationOptions(
            request_json["host"], request_json["strategy"])

        return 'codon optimization options set'
    except Exception as error:
        return {"error": "Encountered error while setting codon optimization options\n" + (
            traceback.format_exc() if __debug__ else "")}


@app.route('/order', methods=['POST'])
def order():
    try:
        request_json = request.get_json()
        if "offers" not in request_json:
            return {"error": "Request is missing fields"}

        return json.jsonify(service.issueOrder(request_json["offers"]))
    except Exception as error:
        return {"error": "Encountered error while issuing order\n" + (
            traceback.format_exc() if __debug__ else "")}
