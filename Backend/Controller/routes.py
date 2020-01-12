import tempfile
from random import random, randint
from time import sleep

from flask import request, json
from werkzeug.utils import secure_filename

from .app import app
from .dataformats import SearchResponse
from .parser import parse
from Pinger.Pinger import *


@app.route('/ping')
def hello_world():
    return 'pong'


@app.route('/vendors')
def get_vendors():
    return json.jsonify({'vendors': ['Twist', 'IDT', 'GenA']})


@app.route('/upload', methods=['post'])
def uploadFile():
    if 'seqfile' not in request.files or request.files['seqfile'] == "":
        return json.jsonify({'error': 'No file specified'})

    resp = SearchResponse()
    for i in range(0, 10):
        vendor_id = randint(0, 1)
        resp.result[0]['offers'].append({
            "vendorinformation": {
                "name": "Twist DNA ..." if vendor_id == 0 else "IDT DNA ...",
                "shortname": "Twist" if vendor_id == 0 else "IDT",
                "key": ""
            },
            "price": random(),
            "turnovertime": randint(1, 20)
        })

    #
    #   TODO: Arr, Here be stuff for populating the response object such as file parsing!
    #
    tempf, tpath = tempfile.mkstemp('.' + secure_filename(request.files['seqfile'].filename).rsplit('.', 1)[1].lower())

    request.files['seqfile'].save(tpath)

    mainPinger = CompositePinger()
    dummyVendor = VendorInformation()
    dummyVendor.key = "Have you ever looked at a pizza and thought: WTF?"
    dummyVendor.name = "There is no SQUIRREL unless SQUIRREL"
    dummyVendor.shortName = "yes"
    dummyPinger = DummyPinger()
    mainPinger.registerVendor(dummyVendor, dummyPinger)
    mainPinger.registerVendor(dummyVendor, dummyPinger)
    mainPinger.registerVendor(dummyVendor, dummyPinger)
    mainPinger.registerVendor(dummyVendor, dummyPinger)

    try:
        # Get sequence information
        objSequences = parse(tpath)

        # Adapt SeqObject to SequenceInformation
        sequences = []
        for seqobj in objSequences:
            seq = SequenceInformation(seqobj.sequence, seqobj.name, seqobj.idN)
            sequences.append(seq)

        # Retrieve offers for all sequences
        # for seq in sequences:
        #    mainPinger.searchOffers({seq.idN, seq.name, seq.sequence})
        #    while mainPinger.isRunning():
        #        sleep(0.01)

        mainPinger.searchOffers(sequences)

        seqoffers = mainPinger.getOffers()

        resp = SearchResponse()
        resp.result = []
        resp.message = []
        resp.count = 0
        resp.offset = 0

        for seqoff in seqoffers:
            result = {
                "sequenceinformation": {"id": seqoff.sequenceInformation.key, "name": seqoff.sequenceInformation.name,
                                        "sequence": seqoff.sequenceInformation.sequence}, "offers": []}

            for offerlist in seqoff.offers:
                for offer in offerlist:
                    result["offers"].append(dict(
                        vendorinformation={"key": offer.vendorInformation.key, "name": offer.vendorInformation.name,
                                           "shortname": offer.vendorInformation.shortName}, price=offer.price.amount,
                        turnovertime=offer.turnovertime))
                    resp.count = resp.count + 1

            resp.result.append(result)
        resp.size = min(20, resp.count)
        return json.jsonify(resp.__dict__)


    except NameError:
        return json.jsonify({'error': 'File format not supported'})
