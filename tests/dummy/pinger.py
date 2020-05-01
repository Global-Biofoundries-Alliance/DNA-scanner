'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
from Pinger.Entities import *
from Pinger.Pinger import *


#
#   The Dummy Pinger is for testing.
#
class DummyPinger(BasePinger):

    def __init__(self):
        self.running = False

        self.tempOffer = Offer(price=Price(
            currency=Currency.EUR, amount=120), turnovertime=14)
        self.tempOffer.messages.append(
            Message(MessageType.DEBUG, "This offer is created from Dummy"))
        self.offers = []

    #
    #   After:
    #       isRunning() -> true
    #       getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer), SequenceOffer(seqInf[1], self.tempOffer), ...
    #                           SequenceOffer(seqInf[n], self.tempOffer)]
    #
    def searchOffers(self, seqInf):
        self.offers = []
        for s in seqInf:
            self.offers.append(SequenceOffers(
                sequenceInformation=s, offers=[self.tempOffer]))
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

    #
    #   Return Order with OrderType Not Supported
    #
    def order(self, offerIds):
        return Order()


class NotAvailablePinger(BasePinger):

    def __init__(self):
        pass

    def searchOffers(self, seqInf):
        raise UnavailableError("This is a unavailable Dummy")

    def isRunning(self):
        return False

    def getOffers(self):
        raise UnavailableError("This is a unavailable Dummy")

    def clear(self):
        pass

    def order(self, seqInf):
        raise UnavailableError("This is a unavailable Dummy")


class AlwaysRunningPinger(BasePinger):

    def __init__(self):
        pass

    def searchOffers(self, seqInf):
        raise IsRunningError("Tis is a running Dummy")

    def isRunning(self):
        return True

    def getOffers(self):
        raise IsRunningError("Tis is a running Dummy")

    def clear(self):
        pass

    def order(self, seqInf):
        raise IsRunningError("Tis is a running Dummy")
