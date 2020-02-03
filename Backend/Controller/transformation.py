from flask import json

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation, SequenceOffers, VendorOffers, SequenceVendorOffers


# Builds a search response in JSON format from a list of offers.
def buildSearchResponseJSON(seqvendoffers, vendors, offset=0, size=10):
    resp = SearchResponse()
    resp.data["result"] = []
    resp.data["globalMessage"] = []
    resp.data["count"] = len(seqvendoffers)
    resp.data["size"] = min(size, len(seqvendoffers) - offset)
    resp.data["offset"] = offset
    for seqvendoff in seqvendoffers[offset: min(offset + size, len(seqvendoffers))]:
        result = {
            "sequenceInformation": {"id": seqvendoff.sequenceInformation.key,
                                    "name": seqvendoff.sequenceInformation.name,
                                    "sequence": seqvendoff.sequenceInformation.sequence,
                                    "length": len(seqvendoff.sequenceInformation.sequence)}, "vendors": []}

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


def filterOffers(filter, seqvendoffers):
    filteredOffers = []
    for seqvendoff in seqvendoffers:
        filteredSeqVendOff = SequenceVendorOffers(seqvendoff.sequenceInformation)
        for vendoff in seqvendoff.vendorOffers:
            filteredVendOff = VendorOffers(vendoff.vendorInformation)
            if "vendors" not in filter or \
                    vendoff.vendorInformation.key in filter["vendors"]:
                for offer in vendoff.offers:
                    if "price" not in filter or \
                            offer.price.amount >= filter["price"][0] and offer.price.amount <= filter["price"][1]:
                        if "deliveryDays" not in filter or \
                                offer.turnovertime <= filter["deliveryDays"]:
                            filteredVendOff.offers.append(offer)

            # Only append structures that actually contain something
            if filteredVendOff.offers:
                filteredSeqVendOff.vendorOffers.append(filteredVendOff)

    return filteredOffers
