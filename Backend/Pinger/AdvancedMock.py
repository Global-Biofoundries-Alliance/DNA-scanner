from .Pinger import *
from random import randint, random

#
#   The Dummy Pinger is for testing.
#
class AdvancedMockPinger(BasePinger):


    def __init__(self, vendorInformation=VendorInformation(name="DummyVendor", shortName="Dummy", key=0)):
        self.running = False

        self.vendorInformation = vendorInformation


        #self.tempOffer = Offer()
        #self.tempOffer.vendorInformation = VendorInformation("Dummy", "DummyVendor", 0)
        #self.tempOffer.price = Price(currency=Currency.EUR)
        #self.tempOffer.price.amount = 120
        #self.tempOffer.turnovertime = 14
        #self.tempOffer.messages.append(Message(MessageType.DEBUG, "This offer is created from Dummy"))
        #self.offers = []

    #
    #   After:
    #       isRunning() -> true
    #       getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer), SequenceOffer(seqInf[1], self.tempOffer), ...
    #                           SequenceOffer(seqInf[n], self.tempOffer)]
    #
    def searchOffers(self, seqInf):
        self.offers = []
        for s in seqInf:
            numOffers = randint(0, 10)
            tempOffers = []
            for i in range(0, numOffers):
                tempOffer = Offer()
                tempOffer.vendorInformation = self.vendorInformation
                tempOffer.price = Price(currency=Currency.EUR, amount=float(int(random() * 100)) / 100)
                tempOffer.turnovertime = randint(0, 20)
                tempOffers.append(tempOffer)
            self.offers.append(SequenceOffers(s, tempOffers))
            #self.offers.append(SequenceOffers(s, [self.tempOffer]))
        self.running = True

    #
    #   True if searchOffers called last
    #   False if getOffers called last
    #
    def isRunning(self):
        return self.running

    #
    #   Returns List with a  SequenceOffer for every sequence in last searchOffers(seqInf)-call.
    #   Every SequenceOffer contains the same offers. Default 1 see self.tempOffer and self.offers.
    #
    def getOffers(self):
        self.running = False
        return self.offers


