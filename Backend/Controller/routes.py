from flask import Flask, request, json, flash
from .app import app
from .dataformats import SearchResponse


@app.route('/upload', methods=['post'])
def uploadFile():
    if 'seqfile' not in request.files:
        flash('No file specified')

    resp = SearchResponse()

    #
    #   TODO: Arr, Here be stuff for populating the response object such as file parsing!
    #

    return json.jsonify(resp.__dict__)
