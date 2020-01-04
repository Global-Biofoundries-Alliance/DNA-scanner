import tempfile
from random import random, randint

from flask import request, json
from werkzeug.utils import secure_filename

from .app import app
from .dataformats import SearchResponse
from .parser import parse


@app.route('/upload', methods=['post'])
def uploadFile():
    # if 'seqfile' not in request.files or request.files['seqfile'] == "":
    #    return json.jsonify({'error': 'No file specified'})

    vendornames = ["Twist DNA", "IDT DNA", "GeneArt"]
    vendorshorts = ["Twist", "IDT", "GenA"]
    sequencenames = ["Detergent", "Spider Silk", "Smoke Flavor", "Insulin"]
    resp = SearchResponse()
    for s in range(0, 100):
        if s > 0:
            resp.result.append({})  # make space for the next result

        resp.result[s]["sequenceinformation"] = {
                    "id": str(randint(0, 9999)) + '-' + str(randint(0, 9999)),
                    "name": sequencenames[randint(0, len(sequencenames) - 1)],
                    "sequence": "ACTG"
                }

        resp.result[s]['offers'] = []
        for i in range(0, 10):
            vendor_id = randint(0, 2)
            resp.result[s]['offers'].append({
                "vendorinformation": {
                    "name": vendornames[vendor_id],
                    "shortname": vendorshorts[vendor_id],
                    "key": ""
                },
                "price": random(),
                "turnovertime": randint(1, 20)
            })
            resp.count = resp.count + 1

    #
    #   TODO: Arr, Here be stuff for populating the response object such as file parsing!
    #
    #tempf, tpath = tempfile.mkstemp('.' + secure_filename(request.files['seqfile'].filename).rsplit('.', 1)[1].lower())


    #request.files['seqfile'].save(tpath)

    #try:
    #    parse(tpath)
    #except NameError:
    #    return json.jsonify({'error': 'File format not supported'})

    return json.jsonify(resp.__dict__)
