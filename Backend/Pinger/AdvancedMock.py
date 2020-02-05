from .Pinger import *
from random import randint, random

#
#   The Dummy Pinger is for testing.
#
class AdvancedMockPinger(BasePinger):


    def __init__(self, vendorInformation=VendorInformation(name="DummyVendor", shortName="Dummy", key=0)):
        self.running = False
        self.offers = []
        self.vendorInformation = vendorInformation

    #
    #   After:
    #       isRunning() -> true
    #       getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer), SequenceOffer(seqInf[1], self.tempOffer), ...
    #                           SequenceOffer(seqInf[n], self.tempOffer)]
    #
    def searchOffers(self, seqInf):
        self.offers = []
        counter = 0
        for s in seqInf:
            numOffers = randint(0, 10)
            tempOffers = []
            for i in range(0, numOffers):
                tempOffer = Offer()
                tempOffer.vendorInformation = self.vendorInformation
                tempOffer.price = Price(currency=Currency.EUR, amount=float(int(random() * 100)) / 100)
                tempOffer.turnovertime = randint(0, 20)
                tempOffer.messages = []
                counter = counter + 1
                tempOffers.append(tempOffer)
            self.offers.append(SequenceOffers(s, tempOffers))
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

    def clear(self):
        self.offers = []
        self.running = False


