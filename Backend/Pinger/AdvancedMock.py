from .Pinger import *
from random import randint, random
import random as rand

#
#   The Dummy Pinger is for testing.
#
class AdvancedMockPinger(BasePinger):


    def __init__(self):
        self.running = False
        self.offers = []

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
                    Message(MessageType.INVALID_LENGTH, "Sequence length invalid"),
                    Message(MessageType.SEQUENCE_TOO_SHORT, "Sequence too short"),
                    Message(MessageType.SEQUENCE_TOO_LONG, "Sequence too long"),
                    Message(MessageType.UNABLE_TO_PRODUCE, "This vendor cannot synthesize this sequence"),
                    Message(MessageType.HOMOLOGY, "Homology problem")]

        self.running = True
        self.offers = []
        counter = 0
        for s in seqInf:
            numOffers = randint(0, 10)
            tempOffers = []
            for i in range(0, numOffers):
                tempOffer = Offer()
                tempOffer.price = Price(currency=Currency.EUR, amount=float(int((random()) * 10000)) / 100)
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
        self.running = False


