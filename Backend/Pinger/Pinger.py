from .Entities import *
from .Validator import entityValidator as Validator


#########################################################
#                                                       #
#   Classes only used inside of the Pinger              #
#                                                       #
#########################################################

#
#   Desc:   Class to make tupples of VendorInformations with VendorPingers.
#
#   @attribute vendor
#       Type  VendorInfomation. Defines the vendor represented by the handler.
#   @attribute handler
#       Type BasePinger. Handles the communication with the API of the vendor represented by attribute vendor.
#
class VendorHandler:
    def __init__(self, vendorInformation, vendorPinger):
        # TODO Check Types
        self.vendor = vendorInformation
        self.handler = vendorPinger

#########################################################
#                                                       #
#   Pinger                                              #
#                                                       #
#   BasePinger: Pinger-Structure to represent           #
#       a sprecific vendor                              #
#                                                       #
#   ManagedPinger: Pinger-Structure with advanced       #
#       functionality. Uses BasePingers to handle       #
#       multiple vendors.                               #
#                                                       #
#########################################################

#
#   Desc:   Interface representing a Vendor-API with unified methods.
#
class BasePinger:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start a search for a given list of sequences. This method has no result because of asynchronous search.
    #           After this method is called it starts searching. isRunning will be true. If the search is finished isRunning()
    #           will return False. Then you can get the full result with getOffers().
    #           Maybe you can get a partial result from getOffers() while running.
    #
    #   @param seqInf
    #           Type ArrayOf(Entities.SequenceInformation). Represent Sequences searching offers for.
    #
    def searchOffers(self, seqInf):
        raise NotImplementedError

    #
    #   Desc:   True if Pinger is currently searching,
    #           else false.
    #
    #   @result 
    #           Boolean. True if searching, else false.
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Desc:   Returns the current offers. If isRunning() is True, then searching is not finished and maybe you can
    #           get a partial result. After searching is finished isRunning() is False and the result will be complete.
    #           Return an Empty Array, if it was not searching before.
    #
    #   @result 
    #           Type ArrayOf(Entities.SequenceOffers). 
    #
    def getOffers(self):
        raise NotImplementedError

    #
    #   Desc:   Resets the pinger by
    #               - stop searching -> isRunning() = false
    #               - resets the offers to a empty list -> getOffers = []
    #
    def clear(self):
        raise NotImplementedError

#
#   Desc:   Interface for represent a fully Pinger. Fully Pinger means managing multiple vendor (represented by
#           BasePingers) and add advanced functionalities e.g. search just for specific vendors.
#

class ManagedPinger:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start a search for a given list of sequences. This method has no result because of asynchronous search.
    #           After this method is called it starts searching. isRunning will be true. If the search is finished isRunning()
    #           will return False. Then you can get the full result with getOffers().
    #           Maybe you can get a partial result from getOffers() while running.
    #
    #   @param seqInf
    #           Type ArrayOf(Entities.SequenceInformation)
    #
    #   @param vendors
    #           Type ArrayOf(int). Search will be started only for vendors, which VendorInformation.key exists in given list. If 
    #           the list is empty, then searching for every vendor.
    #
    def searchOffers(self, seqInf, vendors=[]):
        raise NotImplementedError

    #
    #   Desc:   True if Pinger is currently searching,
    #           else false.
    #
    #   @result 
    #           Type Boolean. True if searching, else false.
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Desc:   Returns the current offers. If isRunning() is True, then searching is not finished and maybe you can
    #           get a partial result. After searching is finished isRunning() is False and the result will be complete.
    #           Return an Empty Array, if it was not searching before.
    #
    #   @result ArrayOf(Entities.SequenceVendorOffers)
    #
    def getOffers(self):
        raise NotImplementedError

    #
    #   Desc:   Register a new Vendor with information and pinger. Then actions like searching for offers can be done
    #           for the vendor.
    #
    #   @param vendorInformation
    #           Type Entities. VendorInformation. Contains the Information of the Vendor. If a vendor with the same key
    #           already exists, the VendorInformation and the Vendor-Pinger will be overriden by the given one.
    #
    #   @param vendorPinger 
    #           Type BasePinger. The Pinger handling the actions for the vendor.
    #
    def registerVendor(self, vendorInformation, vendorPinger):
        raise NotImplementedError

    #
    #   Desc:   Returns all registered vendors.
    #
    #   @return
    #       Type ArrayOf(VendorInformation). List of all registered vendors.
    #
    def getVendors(self):
        raise NotImplementedError


#
#   Desc: A simple Implementation of a ManagedPinger
#
class CompositePinger(ManagedPinger):

    def __init__(self):
        self.vendorHandler = []
        self.sequenceOffers = []

    #
    #   see ManagedPinger.registerVendor
    #
    #   @param vendorInformation
    #       Has type VendorInformation (see Entities.py). If vendorInformation already 
    #       exists, then vendorInformation and vendorPinger overrides the existing one.
    #   @param vendorPinger
    #       Has type BasePinger (see above).
    #
    def registerVendor(self, vendorInformation, vendorPinger):
        # Initialize list if necessary
        if self.vendorHandler is None:
            self.vendorHandler = []

        # Check Input with validator
        if(isinstance(vendorInformation, VendorInformation)):
            if(not Validator.validate(vendorInformation)):
                return
        else:
            print("Invalid Input: vendorInformation has not type VendorInformation")
            return

        if(not isinstance(vendorPinger, BasePinger)):
            print("Invalid Input: vendorPinger has not type BasePinger")
            return

        # if vendor-key already exists, then override this vendorhandler
        if len(self.vendorHandler)>0:
            for counter in range(0, len(self.vendorHandler)):
                if (self.vendorHandler[counter].vendor.key == vendorInformation.key):
                    self.vendorHandler[counter] = VendorHandler(vendorInformation, vendorPinger)
                    return

        # Vendor-key is a new one. 
        # Append the new vendorHandler 
        self.vendorHandler.append(VendorHandler(vendorInformation, vendorPinger))


    #
    #   see ManagedPinger.getVendors
    #
    def getVendors(self):
        result = []
        # TODO musst be update to new definitions
        for vendor in self.vendorHandler:
            result.append(vendor.vendor)
        return result

    #
    #   see ManagedPinger.searchOffers
    #
    def searchOffers(self, seqInf, vendors=[]):
        # check input: seqInf
        if(not isinstance(seqInf, list)):
            print("Parameter seqInf should be a list")
            return
        for seq in seqInf:
            if (not isinstance(seq, SequenceInformation)):
                print("parameter seqInf contains elements which are not of type SequenceInformation")
                return
            if(not Validator.validate(seq)):
                print("SequenceInformation is invalid")
                return
        # check input: vendors
        if (not isinstance(vendors, list)):
            print("parameter vendors should be a list")
            return
        for vendor in vendors:
            if(not isinstance(vendor, int)):
                print("parameter vendors should only contain integers")
                return

        # TODO SequenceVendorOffers
        # initialize empty sequenceOffers
        self.sequenceOffers = []
        for s in seqInf:
            self.sequenceOffers.append(SequenceOffers(s))

        for vh in self.vendorHandler:
            # Start searching if vendor is accepted by the filter
            if(len(vendors) == 0 or vh.vendor.key in vendors):
                vh.handler.searchOffers(seqInf)

            # Clear vendor, if not accepted by the filter
            else:
                vh.handler.clear()

    #
    #   see ManagedPinger.isRunning
    #
    def isRunning(self):

        for vh in self.vendorHandler:
            if vh.handler.isRunning():
                return True

        return False

    #
    #   see ManagedPinger.getOffers
    #
    def getOffers(self):

        # Clear offers
        for s in self.sequenceOffers:
            s.offers = []

        # TODO update to new structure
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
                # append Offers from leaf to local if SequenceKeys are equal
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

    def clear(self):
        self.offers = []
        self.running = False
