from sys import maxsize

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation, VendorOffers, SequenceVendorOffers
from flask import json


# Builds a search response in JSON format from a list of offers.
def buildSearchResponseJSON(seqvendoffers, vendors, selector, offset=0, size=10):
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
            result["vendors"].append({"key": vendor.key, "offers": []})

        # Abysmal starting offer so the first offer will get selected right away
        # NOTE: Do not set this to maxsize! This will break the selection as this uses % maxsize.
        selectedResult = {"price": maxsize - 1, "turnoverTime": maxsize - 1, "offerMessages": [], "selected": False}
        for vendoff in seqvendoff.vendorOffers:
            resultOffers = []
            for offer in vendoff.offers:
                messages = []

                for message in offer.messages:
                    if message.messageType.value in range(1000, 1999) or message.messageType.value in range(4000, 4999):
                        messages.append({"text": message.text, "messageType": message.messageType.value})

                resultOffers.append({
                    "price": offer.price.amount,
                    "turnoverTime": offer.turnovertime,
                    "offerMessage": messages,
                    "selected": False})

            for offer in sorted(resultOffers, key=selector):
                result["vendors"][vendoff.vendorInformation.key]["offers"].append(offer)
            resultList = result["vendors"][vendoff.vendorInformation.key]["offers"]
            selectedResult = selectedResult if resultOffers and \
                                               (selector(selectedResult) <= selector(resultList[0])) else resultList[0]

        selectedResult["selected"] = True

        resp.data["result"].append(result)

    return json.jsonify(resp.data)


# Converts a List[SequenceObject] to a List[SequenceInformation]
def sequenceInfoFromObjects(objSequences):
    sequences = []
    for seqobj in objSequences:
        seq = SequenceInformation(seqobj.sequence, seqobj.name, seqobj.idN)
        sequences.append(seq)
    return sequences


#
#   Receives a filter and a list of SequenceVendorOffers and returns a subset of them that match the filter's criteria
#
#   @param filter the filter settings
#   @param seqvendoffers the offers to filter
#   @result list of the results matching filter
#
def filterOffers(filter, seqvendoffers):
    filteredOffers = []
    for seqvendoff in seqvendoffers:
        filteredSeqVendOff = SequenceVendorOffers(seqvendoff.sequenceInformation, [])
        for vendoff in seqvendoff.vendorOffers:
            filteredVendOff = VendorOffers(vendoff.vendorInformation, [])
            if "vendors" not in filter or \
                    vendoff.vendorInformation.key in filter["vendors"]:
                for offer in vendoff.offers:
                    if "price" not in filter or offer.price.amount < 0 or \
                            offer.price.amount >= filter["price"][0] and offer.price.amount <= filter["price"][1]:
                        if "deliveryDays" not in filter or offer.turnovertime < 0 or \
                                offer.turnovertime <= filter["deliveryDays"]:
                            filteredVendOff.offers.append(offer)

            # Only append structures that actually contain something
            if filteredVendOff.offers:
                filteredSeqVendOff.vendorOffers.append(filteredVendOff)
        filteredOffers.append(filteredSeqVendOff)
    return filteredOffers
