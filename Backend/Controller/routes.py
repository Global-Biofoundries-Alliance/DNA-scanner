import tempfile

from flask import request, json, flash
from werkzeug.utils import secure_filename

from .app import app
from .dataformats import SearchResponse
from .parser import parse

@app.route('/upload', methods=['post'])
def uploadFile():
    if 'seqfile' not in request.files:
        flash('No file specified')

    resp = SearchResponse()

    #
    #   TODO: Arr, Here be stuff for populating the response object such as file parsing!
    #
    tempf = tempfile.mkdtemp('.' + secure_filename(request.files['seqfile'].filename).rsplit('.', 1)[1].lower())
    parse(tempf)

    return json.jsonify(resp.__dict__)