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
class VendorInformation:

    def __init__(self, name = "", shortName = "", key = ""):
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
#   Desc:   Messages with specific type and text
#
class Message:

    def __init__(self, type = MessageType.DEBUG, text = ""):
        self.type = type
        self.text = text



