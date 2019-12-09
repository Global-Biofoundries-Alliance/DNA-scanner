from .Entities import *

#########################################################
#                                                       #
#   Pinger                                              #
#                                                       #
#########################################################


class BasePinger:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start a search for the given sequence. 
    #           Has no result, because asynchronous search.
    #
    def searchOffers(self, seqInf):
        raise NotImplementedError

    #
    #   Desc:   True if pinger is currently searching
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Desc: Returns the current offers. Result can change while searching.
    #
    def getOffers(self):
        raise NotImplementedError


class AbstractPinger(BasePinger):

    #
    #   Desc: Registration of the basepinger handlers of the various vendors
    #
    def registerVender(self, vendorInformation, vendorPinger):
        if self.vendorHandler is None:
            self.vendorHandler = []

        self.vendorHandler.append({ "vendor": vendorInformation, "handler": vendorPinger})


    def getVendors(self):
        result = []
        for vendor in self.vendorHandler:
            result.append(vendor.v)
        return result


class ProductivePinger(AbstractPinger):
        
    def __init__(self):
        print("productive pinger")

    def searchOffers(self, seqInf):
        # TODO Maybe throw error if running or maybe create abort function
        self.offers = []
        for s in seqInf:
            self.sequenceOffers.append(SequenceOffers(s))

        for vh in self.vendorHandler:
            vh.handler.searchOffers(seqInf)


    def isRunning(self):

        for vh in self.vendorHandler:
            if vh.handler.isRunning() == True:
                return True

        return False


    def getOffers(self):
        result = []

        for vh in self.vendorHandler:
            vOffers = vh.handler.getOffers()

            for offer in vOffers:
                for so in self.sequenceOffers:
                    self.sequenceOffers.offers = []

                    if(so.sequenceInformation.key == offer.sequenceInformation.key ):
                        so.offers.append(offer.offers)

        return result


class DummyPinger(AbstractPinger):


    def __init__(self):
        print("dummy pinger")
        self.running = False

        self.offers = Offer()
        self.offers.vendorInformation = VendorInformation("dummy", "DummyVendor", "DummyVendor Not Real GmbH")
        self.offers.price = Price(currency=Currency.EUR)
        self.offers.price.amount = 120
        self.offers.turnovertime = 14
        self.offers.messages.append(Message(MessageType.DEBUG, "This offer is created from Dummy"))

    def searchOffers(seqInf):
        pass

    def isRunning(self):
        return self.running

    def getOffers(self):
        return self.offers

