from flask import json

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation, SequenceOffers

# Builds a search response in JSON format from a list of offers.
def buildSearchResponseJSON(seqoffers, vendors, offset = 0, size = 10):
    resp = SearchResponse()
    resp.data["result"] = []
    resp.data["globalMessage"] = []
    resp.data["count"] = len(seqoffers)
    resp.data["size"] = min(size, len(seqoffers) - offset)
    resp.data["offset"] = offset
    for seqoff in seqoffers[offset: min(offset + size, len(seqoffers))]:
        result = {
            "sequenceInformation": {"id": seqoff.sequenceInformation.key, "name": seqoff.sequenceInformation.name,
                                    "sequence": seqoff.sequenceInformation.sequence, "length": len(seqoff.sequenceInformation.sequence)}, "vendors": []}

        for vendor in vendors:
            result["vendors"].append({"key": vendor["key"], "offers": []})

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

        resp.data["result"].append(result)


    return json.jsonify(resp.data)

# Converts a List[SequenceObject] to a List[SequenceInformation]
def sequenceInfoFromObjects(objSequences):
    sequences = []
    for seqobj in objSequences:
        seq = SequenceInformation(seqobj.sequence, seqobj.name, seqobj.idN)
        sequences.append(seq)
    return sequences

def filterOffers(filter, seqoffers):
    filteredOffers = []
    for seqoffer in seqoffers:
        filteredSeqOffer = SequenceOffers(seqoffer.sequenceInformation, [])
        for offerlist in seqoffer.offers:
            filteredOfferList = []
            for offer in offerlist:
                if offer.vendorInformation.key in filter["vendors"]:
                    if offer.price.amount >= filter["price"][0] and offer.price.amount <= filter["price"][1]:
                        if offer.turnovertime <= filter["deliveryDays"]:
                           filteredOfferList.append(offer)
            filteredSeqOffer.offers.append(filteredOfferList)
        filteredOffers.append(filteredSeqOffer)
    return filteredOffers
