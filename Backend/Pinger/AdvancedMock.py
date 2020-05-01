'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
from random import randint, random

import random as rand

from .Entities import Order, OrderType, UrlRedirectOrder
from .Pinger import *


#
#   The Dummy Pinger is for testing.
#
class AdvancedMockPinger(BasePinger):

    def __init__(self):
        self.running = False
        self.offers = []
        self.vendorMessages = [Message(
            messageType=MessageType.VENDOR_INFO, text="Warning: This is a mock vendor!")]

        #
        #   After:
        #       isRunning() -> true
        #       getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer), SequenceOffer(seqInf[1], self.tempOffer), ...
        #                           SequenceOffer(seqInf[n], self.tempOffer)]
        #

    def searchOffers(self, seqInf):

        messages = [Message(MessageType.SYNTHESIS_ERROR, "Could not synthesize the sequence"),
                    Message(MessageType.INVALID_SEQUENCE, "Invalid sequence"),
                    Message(MessageType.GC_PROBLEM, "GC problem"),
                    Message(MessageType.INVALID_LENGTH,
                            "Sequence length invalid"),
                    Message(MessageType.SEQUENCE_TOO_SHORT,
                            "Sequence too short"),
                    Message(MessageType.SEQUENCE_TOO_LONG,
                            "Sequence too long"),
                    Message(MessageType.UNABLE_TO_PRODUCE,
                            "This vendor cannot synthesize this sequence"),
                    Message(MessageType.HOMOLOGY, "Homology problem")]

        self.running = True
        self.offers = []
        counter = 0
        currency = rand.choice(list(Currency))
        for s in seqInf:
            numOffers = randint(0, 10)
            tempOffers = []
            for i in range(0, numOffers):
                tempOffer = Offer()
                tempOffer.price = Price(currency=currency, amount=float(
                    int((random()) * 10000)) / 100)
                tempOffer.turnovertime = randint(0, 20)
                tempOffer.messages = []
                if random() < 0.1:
                    tempOffer.messages.append(rand.choice(messages))
                counter = counter + 1
                tempOffers.append(tempOffer)
            self.offers.append(SequenceOffers(s, tempOffers))
        self.running = False

    #
    # True iff a search is still running
    #
    def isRunning(self):
        return self.running

    #
    #   Returns List with a  SequenceOffer for every sequence in last searchOffers(seqInf)-call.
    #   Every SequenceOffer contains the same offers. Default 1 see self.tempOffer and self.offers.
    #
    def getOffers(self):
        return self.offers

    def clear(self):
        self.offers = []
        self.vendorMessages = [Message(
            messageType=MessageType.VENDOR_INFO, text="Warning: This is a mock vendor!")]
        self.running = False

    def order(self, offerIds):
        # This must not happen. Crash so it's visible in the tests
        if not offerIds:
            raise RuntimeError
        offerkeys = []
        for seqoffer in self.offers:
            for offer in seqoffer.offers:
                offerkeys.append(offer.key)

        # Basically returns redirect if all IDs are valid and unsupported
        # otherwise
        for id in offerIds:
            if id not in offerkeys:
                # Faux ID leads to non-supported order response
                return Order(OrderType.NOT_SUPPORTED)
        return UrlRedirectOrder("http://www.example.com")

    def getVendorMessages(self):
        return self.vendorMessages

    #
    #   Desc:   Adds a vendor message to this vendor's message store.
    #
    #   @result
    #           Type Message
    #           The message to be added
    #
    def addVendorMessage(self, message):
        self.vendorMessages.append(message)
