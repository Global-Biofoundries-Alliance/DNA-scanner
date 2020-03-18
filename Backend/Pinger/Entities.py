from enum import Enum
from .atomiccounter import *

#########################################################
#                                                       #
#   Static                                              #
#                                                       #
#########################################################

class MessageType(Enum):
    #
    #   1xxx - Synthesis Errors
    #
    #   Desc:   Errors why a vendor can not produce the Sequence
    #

    # General Synthesis Error
    SYNTHESIS_ERROR = 1000
    # Sequence is not valid
    INVALID_SEQUENCE = 1001
    # Extreme high/low GC in some regions or invalid GC Content
    GC_PROBLEM = 1002
    # Sequence has invalid length
    INVALID_LENGTH = 1003
    # Sequence is too short
    SEQUENCE_TOO_SHORT = 1004
    # Sequence is too long
    SEQUENCE_TOO_LONG = 1005
    # Sequence is good, but vendor is unable to produce (maybe it works with optimization)
    UNABLE_TO_PRODUCE = 1006
    # Too many repeats in the sequence
    TOO_MANY_REPEATS = 1007
    # Homology is the existence of shared ancestry between a pair of structures, or genes
    HOMOLOGY = 1008

    #
    #   2xxx - Vendor Error
    #
    #   Desc:   Errors that are not related to the sequence. Mostly technical Error with
    #           the vendor API.
    #
    
    # General Vendor Error
    VENDOR_ERROR = 2000
    # Vendor-API is currently unavailable
    API_CURRENTLY_UNAVAILABLE = 2001
    
    #
    #   3xxx - Internal Error
    #
    #   Desc:   Error in the use of the Pinger. Maybe wrong configured.
    #

    # General Internal Error
    INTERNAL_ERROR = 3000
    # Wrong Credentials configured
    WRONG_CREDENTIALS = 3001
    # Not Allowed. Credentials are ok, but not allowed to request something.
    NOT_ALLOWED = 3002

    #
    #   4xxx - Info
    #
    #   Desc: Just for Information. Maybe not necessary to look inside.
    #

    # General Info
    INFO = 4000
    # Additional Information from the vendor
    VENDOR_INFO = 4001

    #
    #   5xxx - Debug
    #
    #   Desc:   Used for debug messges. Maybe interesting while development.
    #
    
    # General Debug Message
    DEBUG = 5000


#
#   Desc:   Representation of various currencies
#
class Currency(Enum):
    # Euro
    EUR = 0
    # United States Dollar
    USD = 1
    # Currency is unknown
    UNKNOWN = 2

#########################################################
#                                                       #
#   Data-Classes                                        #
#                                                       #
#########################################################


#
#   Desc:   Representation of a Sequence
#
#   @attribute key
#       Type String. Identifies a specific sequence.
#
#   @attribute name
#       Type String. Gives the sequence an human readable name.
#
#   @attribute sequence
#       Type String. The represented sequence.
#
class SequenceInformation:

    # Define counter for IDs
    # Atomic Counter is a threadsafe counter
    idcounter = AtomicCounter

    def __init__(self, sequence, name = "", key = ""):
        # ID of the sequence.
        self.key = key
        # Name of the sequence. Readable representation of the sequence for users
        self.name = name
        # The sequence
        self.sequence = sequence

    #
    #   Static Method to generate a unique id
    #
    def generateId():
        return Offer.idcounter.increment()



        


#
#   Desc:   Represantation of a Vendor
#
#   Every VendorInformation needs key, shortName and name. 
#   
#   @param key
#       Type Integer. Will be used as identifier
#   @param shortname
#       string. Name represent the vendor.
#   @param name
#       string. Fully-Name of the vendor. Can be equal to shortname.
#
class VendorInformation:

    def __init__(self, name, shortName, key):
        # ID of an Vendor. Will be static for every vendor
        self.key = key

        # Full name of the vendor
        self.name = name

        # Short version name of the vendor. Maybe equal to full name.
        self.shortName = shortName

#
#   Desc:   Representation of a price
#
#   @attribute currency
#           Type Currency. The currency of the amount.
#
#   @attribute amount
#           Numeric Value. The amount of the represented price.
#
#   @attribute customerSpecific
#           Type Boolean. If True the price is specified for the customer.
#           If False the price is not for the specific customer.
#
class Price:

    def __init__(self, amount=-1, currency=Currency.EUR, customerSpecific=False):

        # the currency of the price
        self.currency = currency

        # The price
        self.amount = amount

        # Is this price specific for the user
        self.customerSpecific = customerSpecific

#
#   Desc:   Sequence and a list of offers for this sequence
#
#   @attribute vendorOffers
#           Type ArrayOf(VendorOffers). A list of VendorOffers, which represent 
#           a vendor with his offers for the given sequenceInformation.
#
#   @attribute sequenceInformation
#           Type SequenceInformation. A single SequenceInformation represents a 
#           a sequence. 
#
class SequenceVendorOffers:

    def __init__(self, sequenceInformation, vendorOffers = []):

        # Sequence information
        self.sequenceInformation = sequenceInformation

        # Multiple offers for the sequence information
        self.vendorOffers = vendorOffers

#
#   Desc:   Represents a list of offers for a specific sequence. 
#
#   @attribute sequenceInformation
#       Type SequenceInformation. Specifies the Sequence of the offers.
#
#   @attribute offers
#       Type ArrayOf(Offer). Represents the offers for the sequence specified by attribute sequenceInformation.
#
class SequenceOffers:
    def __init__(self, sequenceInformation, offers = []):
        self.sequenceInformation = sequenceInformation
        self.offers = offers

#
#   Desc:   Represents a list of offers for a specific vendor.
#
#   @attribute vendorInformation
#           Type VendorInformation. Represents the Vendor which offers are listed in 'offers'.
#
#   @attribute offers
#           Type ArrayOf(Offer). The list of offers from the vendor represented from 'vendorInformation'.
#
#   @attribute messages
#           Type ArrayOf(Message). Vendor specific Messages (see MessageType 2XXX)
#
class VendorOffers:

    def __init__(self, vendorInformation, offers = [], messages = []):
        self.vendorInformation = vendorInformation
        
        self.offers = offers

        self.messages = messages

#
#   Desc:   Representation of a Offer. A Offer can also only represent a error, when it contains a
#           message with an error type.
#
#   @attribute key
#           Type int. Unique Id to identify the current offer.
#
#
#   @attribute price
#           Type Price. Represents the price of the offer. If less then 0, then no price is available 
#           or price is unknown.
#
#   @attribute turnovertime
#           Type int. Turnovertime is the number of days it needs to synthesize the sequence. If less then 
#           0, then no turnovertime is available or turnovertime is unknown.
#
#   @attribute messages
#           Type ArrayOf(Message). Offer specific messages. Can be used to return debug information
#           or to output errors from the vendor-APIs.
#
class Offer:

    # Define counter for IDs
    # Atomic Counter is a threadsafe counter
    idcounter = AtomicCounter()

    def __init__(self, price=Price(), turnovertime=-1, messages = []):

        # Unique id of the offer
        self.key = Offer.generateId()

        # price of the offer
        self.price = price

        # Time to deliver
        self.turnovertime = turnovertime

        # for example syntesis-errors
        self.messages = messages

    #
    #   Static Method to generate a unique id
    #
    def generateId():
        return Offer.idcounter.increment()

#
#   Desc:   Messages with specific type and text.
#
#   @attribute type
#           Type MessgageType (Enum). Specified the type of the message. By default it is DEBUG.
#   @attribute text
#           Type str. Can contain text additional to the MessageType. By default it is a empty string.
#
class Message:

    def __init__(self, messageType = MessageType.DEBUG, text = ""):
        self.messageType = messageType
        self.text = text


#####################################################
#                                                   #
#   Entities for Ordering                           #
#                                                   #
#   OrderType: Contains the different types         #
#   a order could be.                               #
#                                                   #
#   Order: Description of the generall Data-        #
#   Format equal for every OrderType                #
#                                                   #
#   Concrete Orders are Type specific.              #
#   The dataformat are equal to the order           #
#   and extended by values, that are specific       #
#   needed for that type.                           #
#                                                   #
#####################################################

#
#   Desc:   Types of the way to make the order.
#
class OrderType(Enum):
    # Not supported
    NOT_SUPPORTED = 1
    # By redirect to an specific URL
    URL_REDIRECT = 2

#
#   Desc:   General interface for orders.
#
#   @attribute orderType
#           Type OrderType. The type of the concrete order.
#
class Order:

    def __init__(self, orderType = OrderType.NOT_SUPPORTED):
        self.orderType = orderType

    #
    #   Desc:   Returns the type of the concrete order.
    #
    #   @result
    #           Type OrderType
    #
    def getType(self):
        return self.orderType

#
#   Desc:   Finish the order by redirect to a specific url.
#
#   @attribute url
#           Type String. The redirect url to make the order.
#
#   @attribute orderType
#           Type OrderType. The type of the concrete order.
#
class UrlRedirectOrder(Order):

    #
    #   Desc:   Constructor.
    #
    #   @param url
    #           Type String. The redirect url to make the order.
    #
    def __init__(self, url):
        super().__init__(orderType=OrderType.URL_REDIRECT)
        self.url = url

#####################################################
#                                                   #
#   Errors                                          #
#                                                   #
#####################################################

#
#   Desc:   Input of a used function is not like exxpected. Should be like
#           described in the description.
#
class InvalidInputError(Exception):
    pass

#
#   Desc:   Used if it is not possible to make a request to a specific url.
#           Maybe destination not exists or is temporary unavailable.
#
class UnavailableError(Exception):
    pass

#
#   Desc:   Pinger is running. You cannot make multiple actions at the same 
#           time.
#
class IsRunningError(Exception):
    pass

#
#   Desc:   Authentication failed. Credentials are wrong or has not enough rights.
#
class AuthenticationError(Exception):
    pass
