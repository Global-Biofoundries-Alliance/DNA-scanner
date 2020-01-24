from flask import json

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation

# Builds a search response in JSON format from a list of offers.
def buildSearchResponseJSON(seqoffers, vendors):
    resp = SearchResponse()
    resp.data["result"] = []
    resp.data["globalMessage"] = []
    count = 0
    countDialog = 0
    resp.data["offset"] = 0
    for seqoff in seqoffers:
        result = {
            "sequenceinformation": {"id": seqoff.sequenceInformation.key, "name": seqoff.sequenceInformation.name,
                                    "sequence": seqoff.sequenceInformation.sequence, "length": len(seqoff.sequenceInformation.sequence)}, "vendors": vendors}

        for vendor in result["vendors"]:
            vendor["offers"] = []

        for offerlist in seqoff.offers:
            for offer in offerlist:
                result["vendors"][offer.vendorInformation.key]["offers"].append(
                {
                    "price": offer.price.amount,
                    "turnoverTime": offer.turnovertime,
                    "offerMessage": [],
                    "selected": False,
                }
                )
        count = count + 1

        resp.data["result"].append(result)
    resp.data["count"] = count
    resp.data["size"] = min(20, count)
    return json.jsonify(resp.data)

# Converts a List[SequenceObject] to a List[SequenceInformation]
def sequenceInfoFromObjects(objSequences):
    sequences = []
    for seqobj in objSequences:
        seq = SequenceInformation(seqobj.sequence, seqobj.name, seqobj.idN)
        sequences.append(seq)
    return sequences
