'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
# pylint: disable=dangerous-default-value
# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-nested-blocks
from sys import maxsize
import types

from flask import json

from Controller.dataformats import SearchResponse
from Pinger.Entities import SequenceInformation, VendorOffers, \
    SequenceVendorOffers


def buildSearchResponseJSON(seqvendoffers, vendors, selector=[],
                            globalMessages=[], vendorMessages={}, offset=0,
                            size=10):
    '''
    Builds a search response in JSON format from a list of offers.

    @param
        seqvendoffers List of SequenceVendorOffers as obtained from a
        ManagedPinger

    @param vendors
        List of available vendor IDs

    @param selector
        This may be either a list of selected offer IDs or a lambda that
        functions as a sorting criterion

    @param offset
        At which position to start showing results

    @param size
        How many results to show per page
    '''
    resp = SearchResponse()
    resp.data["result"] = []
    resp.data["globalMessage"] = globalMessages
    resp.data["count"] = len(seqvendoffers)
    # Set the size to the size requested or as high as it goes
    resp.data["size"] = min(size, len(seqvendoffers) - offset)
    resp.data["offset"] = offset

    # Check if this is a lambda. Otherwise it has to be a list.
    selectByLambda = isinstance(selector, types.FunctionType)

    # Put offers and other relevant data into JSON serializable dictionary
    for seqvendoff in seqvendoffers[offset: min(offset + size,
                                                len(seqvendoffers))]:
        result = {
            "sequenceInformation": {
                "id": seqvendoff.sequenceInformation.key,
                "name": seqvendoff.sequenceInformation.name,
                "sequence": seqvendoff.sequenceInformation.sequence,
                "length": len(seqvendoff.sequenceInformation.sequence)},
            "vendors": []}

        # Setup skeleton for per-vendor information
        for vendor in vendors:
            result["vendors"].append({"key": vendor.key, "offers": []})

        # Abysmal starting offer so the first offer will get selected right
        # away
        # NOTE: Do not set this to maxsize! This will break the selection as
        # this uses % maxsize.
        selectedResult = {"price": maxsize - 1, "turnoverTime": maxsize -
                          1, "offerMessage": [], "selected": False}
        for vendoff in seqvendoff.vendorOffers:
            resultOffers = []

            # offerIndex = 0

            for offer in vendoff.offers:
                messages = []

                for message in offer.messages:
                    # Only output messages that are actually errors
                    if message.messageType.value in range(1000, 3999):
                        messages.append(
                            {"text": message.text,
                             "messageType": message.messageType.value})

                resultOffers.append({
                    # TODO Use a user defined currency
                    "price": offer.price.getAmount(offer.price.currency),
                    "currency": offer.price.currency.symbol(),
                    "turnoverTime": offer.turnovertime,
                    "key": offer.key,
                    "offerMessage": messages,
                    "selected": (not selectByLambda) and
                    offer.key in selector})
                # If not selected by lambda use selection list

            # If there is a selection lambda use it to sort offers and select
            # the best one
            # TODO: If offers are selected by list there should be some kind of
            # sorting as well
            if selectByLambda:
                for offer in sorted(resultOffers, key=selector):
                    result["vendors"][
                        vendoff.vendorInformation.key]["offers"].append(
                        offer)
                resultList = result["vendors"][
                    vendoff.vendorInformation.key]["offers"]
                # Compare previously selected result with the best one from
                # this result list
                selectedResult = selectedResult if not resultList or \
                    (selector(selectedResult) <= selector(resultList[0])) \
                    else resultList[0]

            else:
                result["vendors"][vendoff.vendorInformation.key]["offers"] = \
                    resultOffers

        # Only select the best offer if it is valid (otherwise it would select
        # garbage if all offers are invalid in some way)
        if selectedResult["price"] >= 0 \
                and selectedResult["turnoverTime"] >= 0:
            selectedResult["selected"] = True

        # Put it in the outer result object
        resp.data["result"].append(result)

    vendorMessageList = []
    for vendor in vendors:
        key = vendor.key
        messages = []
        if key in vendorMessages.keys():
            messages = [message.text for message in vendorMessages[key]]
        vendorMessageList.append({"vendorKey": key, "messages": messages})

    resp.data["vendorMessage"] = vendorMessageList

    return json.jsonify(resp.data)


def sequenceInfoFromObjects(objSequences):
    '''Converts a List[SequenceObject] to a List[SequenceInformation].'''
    sequences = []
    for seqobj in objSequences:
        seq = SequenceInformation(seqobj.sequence, seqobj.name, seqobj.idN)
        sequences.append(seq)
    return sequences


def filterOffers(fltr, seqvendoffers):
    '''
    Receives a filter and a list of SequenceVendorOffers and returns a subset
    of them that match the filter's criteria

    @param fltr the filter settings
    @param seqvendoffers the offers to filter
    @result list of the results matching filter
    '''
    filteredOffers = []

    # Iterate through the quite deep offer structure.
    for seqvendoff in seqvendoffers:
        filteredSeqVendOff = SequenceVendorOffers(
            seqvendoff.sequenceInformation, [])
        for vendoff in seqvendoff.vendorOffers:
            filteredVendOff = VendorOffers(vendoff.vendorInformation, [])
            # If existent apply the filtering criteria. Otherwise just let
            # everything in.
            if "vendors" not in fltr or \
                    vendoff.vendorInformation.key in fltr["vendors"]:
                for offer in vendoff.offers:
                    if "price" not in fltr or offer.price.amount < 0 or \
                            (offer.price.amount >= fltr["price"][0]
                             and offer.price.amount <= fltr["price"][1]):
                        if "deliveryDays" not in fltr \
                                or offer.turnovertime < 0 \
                                or offer.turnovertime <= fltr["deliveryDays"]:
                            filteredVendOff.offers.append(offer)

            # Only append structures that actually contain something
            if filteredVendOff.offers:
                filteredSeqVendOff.vendorOffers.append(filteredVendOff)
        filteredOffers.append(filteredSeqVendOff)

    return filteredOffers
