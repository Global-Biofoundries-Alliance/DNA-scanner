from flask import json

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation

# Builds a search response in JSON format from a list of offers.
def buildSearchResponseJSON(seqoffers):
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

# Converts a List[SequenceObject] to a List[SequenceInformation]
def sequenceInfoFromObjects(objSequences):
    sequences = []
    for seqobj in objSequences:
        seq = SequenceInformation(seqobj.sequence, seqobj.name, seqobj.idN)
        sequences.append(seq)
    return sequences