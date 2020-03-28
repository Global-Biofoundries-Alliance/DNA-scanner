import types
from sys import maxsize

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation, VendorOffers, SequenceVendorOffers
from flask import json


# Builds a search response in JSON format from a list of offers.
#
# @param
#       seqvendoffers List of SequenceVendorOffers as obtained from a ManagedPinger
#
# @param vendors
#       List of available vendor IDs
#
# @param selector
#       This may be either a list of selected offer IDs or a lambda that functions as a sorting criterion
#
# @param offset
#       At which position to start showing results
#
# @param size
#       How many results to show per page
def buildSearchResponseJSON(seqvendoffers, vendors, selector=[], globalMessages=[], offset=0, size=10):
    resp = SearchResponse()
    resp.data["result"] = []
    resp.data["globalMessage"] = globalMessages
    resp.data["count"] = len(seqvendoffers)
    # Set the size to the size requested or as high as it goes
    resp.data["size"] = min(size, len(seqvendoffers) - offset)
    resp.data["offset"] = offset

    # Check if this is a lambda. Otherwise it has to be a list.
    selectByLambda = isinstance(selector, types.FunctionType)

    vendorMessages = []
    for vendor in vendors:
        vendorMessages.append({"key": vendor.key, "messages": []})

    # Put offers and other relevant data into JSON serializable dictionary
    for seqvendoff in seqvendoffers[offset: min(offset + size, len(seqvendoffers))]:
        result = {
            "sequenceInformation": {"id": seqvendoff.sequenceInformation.key,
                                    "name": seqvendoff.sequenceInformation.name,
                                    "sequence": seqvendoff.sequenceInformation.sequence,
                                    "length": len(seqvendoff.sequenceInformation.sequence)}, "vendors": []}

        # Setup skeleton for per-vendor information
        for vendor in vendors:
            result["vendors"].append({"key": vendor.key, "offers": []})

        # Abysmal starting offer so the first offer will get selected right away
        # NOTE: Do not set this to maxsize! This will break the selection as this uses % maxsize.
        selectedResult = {"price": maxsize - 1, "turnoverTime": maxsize - 1, "offerMessage": [], "selected": False}
        for vendoff in seqvendoff.vendorOffers:
            resultOffers = []
            offerIndex = 0
            for offer in vendoff.offers:
                messages = []

                for message in offer.messages:
                    # Only output messages that are actually errors
                    if message.messageType.value in range(1000, 1999):
                        messages.append({"text": message.text, "messageType": message.messageType.value})

                resultOffers.append({
                    "price": offer.price.amount,
                    "turnoverTime": offer.turnovertime,
                    "key": offer.key,
                    "offerMessage": messages,
                    "selected": (not selectByLambda) and
                                offer.key in selector})  # If not selected by lambda use selection list

            # Avoid message duplication (would be guaranteed with more than one sequence otherwise)
            vendor_messages_unfiltered = [message.text for message in vendoff.messages]
            vendorKey = vendoff.vendorInformation.key
            for vm in vendor_messages_unfiltered:
                if vm not in vendorMessages[vendorKey]["messages"]:
                    vendorMessages[vendorKey]["messages"].append(vm)

            # If there is a selection lambda use it to sort offers and select the best one
            # TODO: If offers are selected by list there should be some kind of sorting as well
            if selectByLambda:
                for offer in sorted(resultOffers, key=selector):
                    result["vendors"][vendoff.vendorInformation.key]["offers"].append(offer)
                resultList = result["vendors"][vendoff.vendorInformation.key]["offers"]
                # Compare previously selected result with the best one from this result list
                selectedResult = selectedResult if not resultList or \
                                                   (selector(selectedResult) <= selector(resultList[0])) else \
                    resultList[0]

            else:
                result["vendors"][vendoff.vendorInformation.key]["offers"] = resultOffers

        # Only select the best offer if it is valid (otherwise it would select garbage if all offers are invalid in some way)
        if selectedResult["price"] >= 0 and selectedResult["turnoverTime"] >= 0:
            selectedResult["selected"] = True

        # Put it in the outer result object
        resp.data["result"].append(result)

    resp.data["vendorMessage"] = vendorMessages

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
    # Iterate through the quite deep offer structure
    for seqvendoff in seqvendoffers:
        filteredSeqVendOff = SequenceVendorOffers(seqvendoff.sequenceInformation, [])
        for vendoff in seqvendoff.vendorOffers:
            filteredVendOff = VendorOffers(vendoff.vendorInformation, [])
            # If existent apply the filtering criteria. Otherwise just let everything in.
            if "vendors" not in filter or \
                    vendoff.vendorInformation.key in filter["vendors"]:
                for offer in vendoff.offers:
                    if "price" not in filter or offer.price.amount < 0 or \
                            (offer.price.amount >= filter["price"][0] and offer.price.amount <= filter["price"][1]):
                        if "deliveryDays" not in filter or offer.turnovertime < 0 or \
                                offer.turnovertime <= filter["deliveryDays"]:
                            filteredVendOff.offers.append(offer)

            # Only append structures that actually contain something
            if filteredVendOff.offers:
                filteredSeqVendOff.vendorOffers.append(filteredVendOff)
        filteredOffers.append(filteredSeqVendOff)
    return filteredOffers
