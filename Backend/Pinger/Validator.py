#########################################################
#                                                       #
#   This file contains an Validator to check            #
#   Entities of the Pinger-package agains their         #
#   definitions.                                        #
#                                                       #
#   Can be used to validate the Input of the Pinger or  #
#   for testing.                                        #
#                                                       #
#########################################################

from .Entities import *
import numbers

class Validator:
    def __init__(self):
        raise NotImplementedError

    def validate(self, obj):
        raise NotImplementedError

class EntityValidator:
    def __init__(self, raiseError=False, errorClass=Exception, printError=False):
        self.raiseError = raiseError
        self.errorClass = errorClass
        self.printError = printError

    def validate(self, obj):
        # VendorInformation
        if isinstance(obj, VendorInformation):
            # Check Types
            if(not isinstance(obj.key, int)):
                return self.raiseFalse("key is not a numeric value")
            if(not isinstance(obj.shortName, str)):
                return self.raiseFalse("shortName is not a String")
            if(not isinstance(obj.name, str)):
                return self.raiseFalse("name is not a String")

        # SequenceInformation
        elif isinstance(obj, SequenceInformation):
            # Check Types
            if(not isinstance(obj.key, str)):
                return self.raiseFalse("key is not a String")
            if(not isinstance(obj.name, str)):
                return self.raiseFalse("name is not a String")
            if(not isinstance(obj.sequence, str)):
                return self.raiseFalse("sequence is not a String")

        # Price
        elif isinstance(obj, Price):
            # Check Types
            if(not isinstance(obj.currency, Currency)):
                return self.raiseFalse("currency is not of type Currency")
            if(not isinstance(obj.amount, numbers.Number)):
                return self.raiseFalse("amount is not a number")
            if(not isinstance(obj.customerSpecific, bool)):
                return self.raiseFalse("customerSpecific is not a boolean")

        # SequenceVendorOffers
        elif isinstance(obj, SequenceVendorOffers):
            if isinstance(obj.sequenceInformation, SequenceInformation):
                if (not self.validate(obj.sequenceInformation)):
                    return raiseFalse("SequenceVendorOffers contains invalid SequenceInformation")
            else:
                return raiseFalse("sequenceInformation is not of type SequenceInformation")
            if isinstance(obj.vendorOffers, VendorOffers):
                if (not self.validate(obj.vendorOffers)):
                    return raiseFalse("SequenceVendorOffers contains invalid VendorOffers")
            else:
                return raiseFalse("vendorOffers is not of type VendorOffers")

        # SequenceOffers
        elif isinstance(obj, SequenceOffers):
            if isinstance(obj.sequenceInformation, SequenceInformation):
                if (not self.validate(obj.sequenceInformation)):
                    return raiseFalse("SequenceOffers contains invalid SequenceInformation")
            else:
                return raiseFalse("sequenceInformation is not of type SequenceInformation")
            if isinstance(obj.offers, list):
                for offer in obj.offers:
                    if isinstance(offer, Offer):
                        if (not self.validate(offer)):
                            return raiseFalse("one offer in offers is invalid")
                    else:
                        return raiseFalse("one object in offers is not of type Offer")
            else:
                return raiseFalse("offers is not of type List")

        # VendorOffers
        elif isinstance(obj, VendorOffers):
            if isinstance(obj.vendorInformation, vendorInformation):
                if (not self.validate(obj.vendorInformation)):
                    return raiseFalse("VendorOffers contains invalid VendorInformation")
            else:
                return raiseFalse("vendorInformation is not of type VendorInformation")
            if isinstance(obj.offers, list):
                for offer in obj.offers:
                    if isinstance(offer, Offer):
                        if (not self.validate(offer)):
                            return raiseFalse("one offer in offers is invalid")
                    else:
                        return raiseFalse("one object in offers is not of type Offer")
            else:
                return raiseFalse("offers is not of type List")
        
        # Offer
        elif isinstance(obj, Offer):
            # price
            if (not isinstance(obj.price, Price)):
                return raiseFalse("Attribute price is not of type Price")
            if (not self.validate(obj.price)):
                return raiseFalse("Attribute price is invalid")
            
            #turnovertime
            if (not isinstance(obj.turnovertime, int)):
                return raiseFalse("turnovertime is not of type int")
            
            # messages
            if isinstance(obj.messages, list):
                for message in obj.messages:
                    if isinstance(message, Message):
                        if (not self.validate(message)):
                            return raiseFalse("one message in messages is invalid")
                    else:
                        return raiseFalse("one object in message is not of type Message")
            else:
                return raiseFalse("messages is not of type List")

        # Message
        elif isinstance(obj, Message):
            if(not isinstance(obj.messageType, MessageType)):
                return raiseFalse("attribute type of Message has not type MessageType")
            if(not isinstance(obj.text, str)):
                return raiseFalse("text is not of type String")

        # List
        elif isinstance(obj, list):
            for elem in obj:
                if (not self.validate(elem)):
                    return self.raiseFalse("List contains invalid elements")

        else:
            return self.raiseFalse("The object to validate has a not supported type")

        return self.raiseTrue()

    def raiseFalse(self, text = ""):
        if self.printError:
            print("Validation Failed:", text)
        if self.raiseError:
            raise errorClass("Validation Failed: ", text)
        return False

    def raiseTrue(self, text = ""):
        return True

class InvalidInputError(Exception):
    pass

entityValidatorThrowing = EntityValidator(raiseError=True, errorClass=InvalidInputError)
entityValidator = EntityValidator()
