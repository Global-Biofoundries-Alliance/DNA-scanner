from .Entities import *


#########################################################
#                                                       #
#   Classes only used inside of the Pinger              #
#                                                       #
#########################################################

class VendorHandler:
    def __init__(self, vendorInformation, vendorPinger):
        self.vendor = vendorInformation
        self.handler = vendorPinger

#########################################################
#                                                       #
#   Pinger                                              #
#                                                       #
#########################################################

#
#   Composite Pattern
#   Client & Component: BasePinger
#   Composite: CompositePattern
#   Leaf: The implemented BasePinger for an specific Vendor.
#   Operations; See the functions of BasePinger
#

class BasePinger:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start a search for a given list of sequences. This method has no result because of asynchronous search.
    #           After call this method it starts searching. isRunning will be true. If the search is finished isRunning()
    #           will return False. Then you can get the full result with getOffers().
    #           Maybe you can get a partially result from getOffers() while running.
    #
    def searchOffers(self, seqInf):
        raise NotImplementedError

    #
    #   Desc:   True if Pinger is currently searching,
    #           else false.
    #   Result-Type: Boolean
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Desc:   Returns the current offers. If isRunning() is True, then searching is not finished and maybe you can
    #           get partially result. After searching is finished isRunning() is False and the result will be complete.
    #   Result-Type: [SequenceOffers, ...]
    #
    def getOffers(self):
        raise NotImplementedError



#
#   Desc: Allows the registration of pingers and forward actions and joins the return-values.
#
class CompositePinger(BasePinger):

    def __init__(self):
        self.vendorHandler = []
        self.sequenceOffers = []

    #
    #   Desc: Registration of the basepinger handlers of the various vendors
    #
    def registerVendor(self, vendorInformation, vendorPinger):
        if self.vendorHandler is None:
            self.vendorHandler = []

        self.vendorHandler.append(VendorHandler(vendorInformation, vendorPinger))


    #
    #   Desc: Returns all Vendor Informations in an list
    #   Result-Type: [VendorInformation, ...]
    #
    def getVendors(self):
        result = []
        for vendor in self.vendorHandler:
            result.append(vendor.vendor)
        return result

    #
    #   Desc:   Start searching in every vendor pinger.
    #
    def searchOffers(self, seqInf):

        self.sequenceOffers = []
        for s in seqInf:
            self.sequenceOffers.append(SequenceOffers(s))

        for vh in self.vendorHandler:
            vh.handler.searchOffers(seqInf)

    #
    #   Desc:   True if one or more Pinger are searching.
    #           False if all Vendor Pinger are finished.
    #   Result-Type: Boolean
    #
    def isRunning(self):

        for vh in self.vendorHandler:
            if vh.handler.isRunning():
                return True

        return False

    #
    #   Desc:   Returns the joined offers from every vendor.
    #   Result-Type: [SequenceOffers, ...]
    #
    def getOffers(self):

        # Clear offers
        for s in self.sequenceOffers:
            s.offers = []

        # Load offers from Vendor-Pingers
        leafSeqOffers = []
        for vh in self.vendorHandler:
            vOffers = vh.handler.getOffers()
            leafSeqOffers.extend(vOffers)

        # For every SequenceOffer from Leaf
        for leafSeqOffer in leafSeqOffers:
            # ... get the Key of the SequenceInformation
            seqKey = leafSeqOffer.sequenceInformation.key

            # ... and for every local SequenceOffer ...
            for seqOffer in self.sequenceOffers:
                # apend Offers from leaf to lokal if SequenceKeys are equal
                if seqOffer.sequenceInformation.key == seqKey:
                    seqOffer.offers.append(leafSeqOffer.offers)

        return self.sequenceOffers

#
#   The Dummy Pinger is for testing.
#
class DummyPinger(BasePinger):


    def __init__(self):
        self.running = False


        self.tempOffer = Offer()
        self.tempOffer.vendorInformation = VendorInformation("dummy", "DummyVendor", "DummyVendor Not Real GmbH")
        self.tempOffer.price = Price(currency=Currency.EUR)
        self.tempOffer.price.amount = 120
        self.tempOffer.turnovertime = 14
        self.tempOffer.messages.append(Message(MessageType.DEBUG, "This offer is created from Dummy"))
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
            self.offers.append(SequenceOffers(s, [self.tempOffer]))
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


