#########################################################
#                                                       #
#   Static                                              #
#                                                       #
#########################################################

class MessageType(Enum):
    # Vendor cannot synthesize the sequence
    SYNTHESIS_ERROR = 0
    # For Example: Vendor API is currently unavailable
    VENDOR_ERROR = 1
    # Just informational message
    INFO = 2
    # Message for debugging
    DEBUG = 3
    # Pinger Internal Error
    INTERNAL_ERROR = 4

#########################################################
#                                                       #
#   Data-Classes                                        #
#                                                       #
#########################################################


#
#   Desc: Representation of a Sequence
#
class SequenzInformation:

    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

    # ID of the sequence. TODO Autogenerate if not set
    key = ""
    # Name of the sequence. Readable representation of the sequence for users 
    name = ""
    # The sequence
    sequence = ""

    # TODO add an toJSON for serializable

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

#
#   Desc: Represantation of a Vendor
#
class VendorInformation:

    def __init__(self, key, name, shortName):
        self.key = key
        self.name = name
        self.shortName = shortName
    
    # ID of an Vendor. Will be static for every vendor
    key = ""
    # Full name of the vendor
    name = ""
    # Short version name of the vendor. Maybe equal to full name.
    shortName = ""

#
#   Desc: Representation of a price
#
class Price:

    # The price
    amount = 0

    # the currency of the price
    currency = "EUR"

    # Is this price specific for the user
    customerSpecific = false


class Offer:

    def __init__(self):
        pass

    # sequence of the offer
    sequenceInformation = {}

    # vendor of the offer
    vendorInformation = {}

    # price of the offer
    price = {}

    # for example syntesis-errors
    messages = []

class Message:
    msgType = MessageType.DEBUG
    value = ""
