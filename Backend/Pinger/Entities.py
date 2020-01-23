from enum import Enum

#########################################################
#                                                       #
#   Static                                              #
#                                                       #
#########################################################

class MessageType(Enum):
    # Vendor can not synthesize the sequence
    SYNTHESIS_ERROR = 0
    # For Example: Vendor API is currently unavailable
    VENDOR_ERROR = 1
    # Just informational message
    INFO = 2
    # Message for debugging
    DEBUG = 3
    # Pinger Internal Error
    INTERNAL_ERROR = 4

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


# Type of the way to make the order
class PurchaseType(Enum):
    # By Shopping Card
    SHOPPING_CARD = 0
    # Not supported
    NOT_SUPPORTED = 1
    # By redirect to an specific URL
    URL_REDIRECT = 2


# Specific currencies
class Currency(Enum):
    # Euro
    EUR = 0

#########################################################
#                                                       #
#   Data-Classes                                        #
#                                                       #
#########################################################


#
#   Desc: Representation of a Sequence
#
class SequenceInformation:

    def __init__(self, sequence, name = "", key = ""):
        # ID of the sequence.
        self.key = key
        # Name of the sequence. Readable representation of the sequence for users
        self.name = name
        # The sequence
        self.sequence = sequence


#
#   Desc: Represantation of a Vendor
#
#   Every VendorInformation needs key, shortName and name. 
#   
#   @param key
#       numeric value. Will be used as identifier
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
#   Desc: Representation of a price
#
class Price:

    def __init__(self, amount=0, currency=Currency.EUR, customerSpecific=False):

        # the currency of the price
        self.currency = currency

        # The price
        self.amount = amount

        # Is this price specific for the user
        self.customerSpecific = customerSpecific

#
#   Desc:   Sequence and a list of offers for this sequence
#
class SequenceOffers:

    def __init__(self, sequenceInformation, offers = []):

        # Sequence information
        self.sequenceInformation = sequenceInformation

        # Multiple offers for the sequence information
        self.offers = offers

#
#   Desc:   Representation of a Offer
#
class Offer:

    def __init__(self, vendorInformation = {}, price = {}, messages = [], turnovertime = -1):

        ### Removed for class SequenceOffers
        # sequence of the offer
        # sequenceInformation = {}

        # vendor of the offer
        self.vendorInformation = vendorInformation

        # price of the offer
        self.price = price

        # Time to deliver
        self.turnovertime = turnovertime

        # for example syntesis-errors
        self.messages = messages

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



