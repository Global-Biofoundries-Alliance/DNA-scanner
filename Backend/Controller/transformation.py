from flask import json

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation, SequenceOffers

# Builds a search response in JSON format from a list of offers.
def buildSearchResponseJSON(seqvendoffers, vendors, offset = 0, size = 10):
    resp = SearchResponse()
    resp.data["result"] = []
    resp.data["globalMessage"] = []
    resp.data["count"] = len(seqvendoffers)
    resp.data["size"] = min(size, len(seqvendoffers) - offset)
    resp.data["offset"] = offset
    for seqvendoff in seqvendoffers[offset: min(offset + size, len(seqvendoffers))]:
        result = {
            "sequenceInformation": {"id": seqvendoff.sequenceInformation.key, "name": seqvendoff.sequenceInformation.name,
                                    "sequence": seqvendoff.sequenceInformation.sequence, "length": len(seqvendoff.sequenceInformation.sequence)}, "vendors": []}

        for vendor in vendors:
            result["vendors"].append({"key": vendor["key"], "offers": []})

        for vendoff in seqvendoff.vendorOffers:
            for offer in vendoff.offers:
                messages = []
                for message in offer.messages:
                    if message.messageType.value in range(1000, 1999):
                        messages.append({"text": message.text, "messageType": message.messageType.value})

                result["vendors"][vendoff.vendorInformation.key]["offers"].append({
                    "price": offer.price.amount,
                    "turnoverTime": offer.turnovertime,
                    "offerMessage": messages})

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
