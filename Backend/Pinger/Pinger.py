from .Entities import *
from .Validator import entityValidatorThrowing as Validator


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


    #
    #   Desc:   Contructor.
    #           The constructor of implemented BasePinger will have specfic parameters. For Example baseUrl and Credentials.
    #
    #           !!! You have to check the costructor for each specific BasePinger of the providers separately, because this is
    #           !!! the only method which cannot be defined uniformly.
    #
    #
    #   @throws AuthenticationError
    #           if credentials are not available, wrong or does not allow access.
    #
    #   @throws UnavailableError
    #           if authentication response not matches pattern or not received.
    #           Maybe the base url of the API is wrong? API could be only temporary
    #           unavailable.
    #
    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start search for offers of a given list of sequences. This method has no result because of asynchronous search.
    #           After this method is called it starts searching. isRunning will be true. If the search is finished isRunning()
    #           will return False. Then you can get the full result with getOffers().
    #           Maybe you can get a partial result from getOffers() while running.
    #
    #   @param seqInf
    #           Type ArrayOf(Entities.SequenceInformation). Represent Sequences searching offers for. Sequence-Keys must be unique.
    #
    #   @throws InvalidInputError
    #           if input parameter are not like expected (see parameter definition above).
    #
    #   @throws IsRunningError
    #           if the Pinger is already running. You have to wait until it is finished.
    #
    #   @throws UnavailableError
    #           if authentication response not matches pattern or not received.
    #           Maybe the base url of the API is wrong? API could be only temporary
    #           unavailable.
    #
    def searchOffers(self, seqInf):
        raise NotImplementedError

    #
    #   Desc:   True if Pinger is currently in progress,
    #           else false.
    #
    #   @result 
    #           Boolean. True if in progress, else false.
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Desc:   Returns the current offers. If isRunning() is True, then searching is not finished and maybe you can
    #           get a partial result. After searching is finished isRunning() is False and the result will be complete.
    #
    #   @result 
    #           Type ArrayOf(Entities.SequenceOffers). Number of SequenceOffers are equal to the number
    #           of sequences from the last call of searchOffers(seqInf). For every sequenceInformation from 
    #           the last searchOffers(seqInf) call exists exactly one SequenceOffer. SequenceOffers must be available, 
    #           even if there is no offer for the sequence. Empty Array, if it was not searching before.
    #
    #   @throws UnavailableError
    #           if authentication response not matches pattern or not received.
    #           Maybe the base url of the API is wrong? API could be only temporary
    #           unavailable.
    #
    def getOffers(self):
        raise NotImplementedError

    #
    #   Desc:   Resets the pinger by
    #               - stop searching -> isRunning() = false
    #               - resets the offers to a empty list -> getOffers = []
    #           Dependent on the method of parallelism it is maybe just waiting for finish running.
    #
    def clear(self):
        raise NotImplementedError

    #
    #   Desc:   Create a request to trigger an order.
    #
    #   @param offerIds
    #           Type ArrayOf(int). Id of the Offer to Order. Ids must be unique.
    #
    #   @results
    #           Type Entities.Order. Representation of the order. A Order can have different sub-types
    #           Your can find more for the various sub-types of orders in Entities.py.
    #
    #   @throws InvalidInputError
    #           if input parameter are not like expected (see parameter definition above).
    #
    #   @throws IsRunningError
    #           if the Pinger is already running. You have to wait until it is finished.
    #
    #   @throws UnavailableError
    #           if authentication response not matches pattern or not received.
    #           Maybe the base url of the API is wrong? API could be only temporary
    #           unavailable.
    #
    def order(self, offerIds):
        raise NotImplementedError



#
#   Desc:   Interface for represent a fully Pinger. Fully Pinger means managing multiple vendor (represented by
#           BasePingers) and add advanced functionalities e.g. search offers only for specific vendors.
#
class ManagedPinger:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start a searching offers for a given list of sequences. This method has no result because of asynchronous search.
    #           After this method is called it starts searching. isRunning will be true. If the search is finished isRunning()
    #           will return False. Then you can get the full result with getOffers().
    #           Maybe you can get a partial result from getOffers() while running.
    #
    #   @param seqInf
    #           Type ArrayOf(Entities.SequenceInformation). Representation of the sequences you want offers for.
    #           Sequence-Keys must be unique.
    #
    #   @param vendors
    #           Type ArrayOf(int). Search will be started only for vendors, which VendorInformation.key exists in given list. If 
    #           the list is empty, then searching for every vendor. Vendor-Keys must be unique. If vendor is not registered it 
    #           will be ignored.
    #
    #   @throws InvalidInputError
    #           if input parameter are not like expected (see parameter definition above).
    #
    #   @throws IsRunningError
    #           if the Pinger is already running. You have to wait until it is finished.
    #
    def searchOffers(self, seqInf, vendors=[]):
        raise NotImplementedError

    #
    #   Desc:   True if Pinger is currently in progress,
    #           else false.
    #
    #   @result 
    #           Type Boolean. True if in progress, else false.
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Desc:   Returns the current offers. If isRunning() is True, then searching is not finished and maybe you can
    #           get a partial result. After searching is finished isRunning() is False and the result will be complete.
    #           Return an Empty Array, if it was not searching before.
    #
    #   @result ArrayOf(Entities.SequenceVendorOffers). For each sequence passed in the seachOffer(seqInf, vendor) call,
    #           there is exactly one SequenceVendorOffer-Object in the array. It contains one VendorOffer for every vendor
    #           included in searchOffers. If a VendorPinger raises an Error, then the VendorOffer will contain a 
    #           ErrorMessage and no offers. 
    #           Vendors excluded by the filter while calling searchOffers wont have VendorOffer.
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
    #   @throws InvalidInputError
    #           if input parameter are not like expected (see parameter definition above).
    #
    def registerVendor(self, vendorInformation, vendorPinger):
        raise NotImplementedError

    #
    #   Desc:   Returns all registered vendors.
    #
    #   @return
    #           Type ArrayOf(VendorInformation). List of all registered vendors. If there is no registered vendor it returns
    #           a empty list [].
    #
    def getVendors(self):
        raise NotImplementedError

    #
    #   Desc:   Create a request to trigger an order with an specific vendor.
    #
    #   @param orderIds
    #           Type ArrayOf(int). Id of the Offer to Order. Ids must be unique.
    #
    #   @param vendor
    #           Type int. The key (VendorInformatin.Key) of the vendor where you want to do the order.
    #
    #   @result
    #           Type Entities.Order. Representation of the order. A Order can have different sub-types
    #           Your can find more for the various sub-types of orders in Entities.py.
    #
    #   @throws InvalidInputError
    #           if input parameter are not like expected (see parameter definition above)
    #           or if parameter vendor does not match any key of registered vendors.
    #
    #   @throws IsRunningError
    #           if the Pinger is already running. You have to wait until it is finished.
    #
    def order(self, offerIds, vendor):
        raise NotImplementedError


#
#   Desc: A simple Implementation of a ManagedPinger
#
class CompositePinger(ManagedPinger):

    def __init__(self):
        self.vendorHandler = []
        self.sequenceVendorOffers = []
        self.vendorMessages = {}
        self.curVendors = []

    #
    #   see ManagedPinger.registerVendor
    #
    def registerVendor(self, vendorInformation, vendorPinger):
        # Initialize list if necessary
        if self.vendorHandler is None:
            self.vendorHandler = []

        # Check Input with validator
        if(isinstance(vendorInformation, VendorInformation)):
            Validator.validate(vendorInformation)
        else:
            raise InvalidInputError("Invalid Input: vendorInformation has not type VendorInformation")

        if(not isinstance(vendorPinger, BasePinger)):
            raise InvalidInputError("Invalid Input: vendorPinger has not type BasePinger but" + str(type(vendorPinger)))

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
        for vendor in self.vendorHandler:
            result.append(vendor.vendor)
        return result

    #
    #   see ManagedPinger.searchOffers
    #
    def searchOffers(self, seqInf, vendors=[]):
        # Check pinger is not running
        if(self.isRunning()):
            raise IsRunningError("Pinger is currently running and can not perform a other action")

        # check input: seqInf
        if(isinstance(seqInf, list)):
            Validator.validate(seqInf)

        for seq in seqInf:
            if (not isinstance(seq, SequenceInformation)):
                raise InvalidInputError("parameter seqInf contains elements which are not of type SequenceInformation")
        # check input: vendors
        if (not isinstance(vendors, list)):
            raise InvalidInputError("parameter vendors should be a list")
        for vendor in vendors:
            if(not isinstance(vendor, int)):
                raise InvalidInputError("parameter vendors should only contain integers")

        # reset vendorMessages
        self.vendorMessages = {}
        self.curVendors = vendors

        # initialize empty sequenceOffers
        self.sequenceVendorOffers = []
        for s in seqInf:
            self.sequenceVendorOffers.append(SequenceVendorOffers(s))

        for vh in self.vendorHandler:
            # Start searching if vendor is accepted by the filter
            if(len(vendors) == 0 or vh.vendor.key in vendors):
                try:
                    vh.handler.searchOffers(seqInf)
                except InvalidInputError as e:
                    # store Message and return when calling getOffers()
                    self.vendorMessages[vh.vendor.key] = [Message(messageType = MessageType.INTERNAL_ERROR, text = str(e))]
                except UnavailableError as e:
                    self.vendorMessages[vh.vendor.key] = [Message(messageType = MessageType.API_CURRENTLY_UNAVAILABLE, text = str(e))]
                except IsRunningError as e:
                    self.vendorMessages[vh.vendor.key] = [Message(messageType = MessageType.INTERNAL_ERROR, text = str(e))]

            # Clear vendor, if not accepted by the filter
            else:
                vh.handler.clear()

    #
    #   see ManagedPinger.isRunning
    #
    def isRunning(self):

        # If one or more vendors are running, then CompositePinger is running
        for vh in self.vendorHandler:
            if vh.handler.isRunning():
                return True

        # No vendor is running
        return False

    #
    #   see ManagedPinger.getOffers
    #
    def getOffers(self):

        # Clear offers
        for s in self.sequenceVendorOffers:
            s.vendorOffers = []

        # Load offers from Vendor-Pingers
        for vh in self.vendorHandler:
            vendorMessage = []
            seqOffers = []

            # Check if vendor-message is available. Vendor messages can be available if a error occured calling searchOffers(...) 
            # at the specific vendor-pinger.
            if vh.vendor.key in self.vendorMessages:
                vendorMessage = self.vendorMessages[vh.vendor.key]
            else:
                seqOffers = vh.handler.getOffers()

            # If output if the VendorPinger is invalid, then ignore and continue
            if (not isinstance(seqOffers, list)):
                print("CompositePinger.getOffers(...): Vendor", vh.vendor.name, "returns", type(seqOffers), "instead of list")
                continue

            # Check the output of the vendor pinger to make sure to return valid output
            try:
                Validator.validate(seqOffers)

                for newSO in seqOffers:

                    for curSO in self.sequenceVendorOffers:
                        if newSO.sequenceInformation.key == curSO.sequenceInformation.key:
                            curSO.vendorOffers.append(VendorOffers(vendorInformation=vh.vendor, offers=newSO.offers, messages = vendorMessage))
            except InvalidInputError:
                # If Invalid values was found ignore this vendor and coninue with the next one
                print("CompositePinger.getOffers(...): Vendor", vh.vendor.name, "returns invalid offers")
                continue
            
            # If vendor has no sequence offers and filter allows the current selected vendor
            # then create the VendorOffer and save it
            if(len(seqOffers) == 0 and (len(self.curVendors) == 0 or vh.vendor.key in self.curVendors)):
                for curSO in self.sequenceVendorOffers:
                    curSO.vendorOffers.append(VendorOffers(vh.vendor, offers=seqOffers, messages = vendorMessage))

        return self.sequenceVendorOffers

    #
    #   see ManagedPinger.order
    #
    def order(self, offerIds, vendor):
        # Check pinger is not running
        if(self.isRunning()):
            raise IsRunningError("Pinger is currently running and can not perform a other action")

        # check input: seqInf
        if(not isinstance(offerIds, list)):
            raise InvalidInputError("parameter vendorIds has not type list")
        for offerId in offerIds:
            if (not isinstance(offerId, int)):
                raise InvalidInputError("parameter vendorIds contains elements which are not of type integer")
        # check input: vendors
        if(not isinstance(vendor, int)):
                raise InvalidInputError("parameter vendor should be a integer")

        # find VendorPinger and call order
        for vh in self.vendorHandler:
            # Start searching if vendor is accepted by the filter
            if(vh.vendor.key == vendor):
                return vh.handler.order(offerIds)

        raise InvalidInputError("Parameter vendor does not match any key of a registered vendor")

