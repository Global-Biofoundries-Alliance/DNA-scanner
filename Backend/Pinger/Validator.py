'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
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

import numbers

from .Entities import Currency, InvalidInputError, \
    Message, MessageType, Offer, Price, SequenceInformation, \
    SequenceOffers, SequenceVendorOffers, VendorInformation, VendorOffers


#
#   Desc:   Interface of a standard Validator
#
#   @method validate(obj: Any): boolean
#
class Validator:

    #
    #   Desc:   Constructor
    #           Can be various for every concrete Validator
    #
    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Validates the given Obj. What it validates is specfic to the concrete
    #           Validator.
    #
    #   @param obj
    #           Any Type. The Object to validate.
    #
    #   @result
    #           True if given obj is valid. False or Error if obj is invalid.
    #           If a error occurs depends on the concrete validator.
    #
    def validate(self, obj):
        raise NotImplementedError

#
#   Desc:   A Concrete Validator to validate Entities from the Pinger Library.
#
#           You can configure the validator to print the errors to the console or
#           to raise a specific errors. To configure set the specific variables
#           in the constructor.
#


class EntityValidator(Validator):

    #
    #   Desc:   Constructor
    #
    #   @param raiseError
    #           Default False. If True the validator will raise errors when a
    #           object to validate is invalid.
    #
    #   @param errorClass
    #           The class of the error thrown if raiseError is True.
    #
    #   @param printError
    #           If True error messages will be printed to the console. If False
    #           nothing will be printed to the console.
    #
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
                    return self.raiseFalse("SequenceVendorOffers contains invalid SequenceInformation")
            else:
                return self.raiseFalse("sequenceInformation is not of type SequenceInformation")
            if isinstance(obj.vendorOffers, list):
                for vendorOffers in obj.vendorOffers:
                    if isinstance(vendorOffers, VendorOffers):
                        if (not self.validate(vendorOffers)):
                            return self.raiseFalse("SequenceVendorOffers contains invalid VendorOffers")
                    else:
                        return self.raiseFalse("vendorOffers has elements with other type than VendorOffer")
            else:
                return self.raiseFalse("vendorOffers is not of type list")

        # SequenceOffers
        elif isinstance(obj, SequenceOffers):
            if isinstance(obj.sequenceInformation, SequenceInformation):
                if (not self.validate(obj.sequenceInformation)):
                    return self.raiseFalse("SequenceOffers contains invalid SequenceInformation")
            else:
                return self.raiseFalse("sequenceInformation is not of type SequenceInformation")
            if isinstance(obj.offers, list):
                for offer in obj.offers:
                    if isinstance(offer, Offer):
                        if (not self.validate(offer)):
                            return self.raiseFalse("one offer in offers is invalid")
                    else:
                        return self.raiseFalse("one object in offers is not of type Offer")
            else:
                return self.raiseFalse("offers is not of type List")

        # VendorOffers
        elif isinstance(obj, VendorOffers):
            # vendorInformation
            if isinstance(obj.vendorInformation, VendorInformation):
                if (not self.validate(obj.vendorInformation)):
                    return self.raiseFalse("VendorOffers contains invalid VendorInformation")
            else:
                return self.raiseFalse("vendorInformation is not of type VendorInformation")

            # offers
            if isinstance(obj.offers, list):
                for offer in obj.offers:
                    if isinstance(offer, Offer):
                        if (not self.validate(offer)):
                            return self.raiseFalse("one offer in offers is invalid")
                    else:
                        return self.raiseFalse("one object in offers is not of type Offer")
            else:
                return self.raiseFalse("offers is not of type List")

        # Offer
        elif isinstance(obj, Offer):
            # key
            if (not isinstance(obj.key, int)):
                return self.raiseFalse("key is not of type int")

            # price
            if (not isinstance(obj.price, Price)):
                return self.raiseFalse("Attribute price is not of type Price")
            if (not self.validate(obj.price)):
                return self.raiseFalse("Attribute price is invalid")

            # turnovertime
            if (not isinstance(obj.turnovertime, int)):
                return self.raiseFalse("turnovertime is not of type int")

            # messages
            if isinstance(obj.messages, list):
                for message in obj.messages:
                    if isinstance(message, Message):
                        if (not self.validate(message)):
                            return self.raiseFalse("one message in messages is invalid")
                    else:
                        return self.raiseFalse("one object in message is not of type Message")
            else:
                return self.raiseFalse("messages is not of type List")

        # Message
        elif isinstance(obj, Message):
            if(not isinstance(obj.messageType, MessageType)):
                return self.raiseFalse("attribute type of Message has not type MessageType")
            if(not isinstance(obj.text, str)):
                return self.raiseFalse("text is not of type String")

        # List
        elif isinstance(obj, list):
            # Check that all elements in the list have the same type and that
            # keys are unique

            elemType = None
            firstElem = True
            keys = []

            # For every element in the list...
            for elem in obj:
                # ... check that it is valide
                if (not self.validate(elem)):
                    return self.raiseFalse("List contains invalid elements")

                if firstElem:
                    # Take the type of the first element to compare with the
                    # other types
                    elemType = type(elem)
                    firstElem = False
                elif elemType != type(elem):
                    # Can be ok because of polymorphism, but currently there is no reason
                    # Maybe remove this later
                    return self.raiseFalse("List contains various types")

                # Check that keys are unique for specific types
                if (isinstance(elem, SequenceInformation)
                        or isinstance(elem, VendorInformation)
                        or isinstance(elem, Offer)):
                    if elem.key in keys:
                        return self.raiseFalse("Identifier is not unique")

                    keys.append(elem.key)

        else:
            return self.raiseFalse("The object to validate has a not supported type")

        return self.raiseTrue()

    #
    #   Desc:   Called if validation failed.
    #
    #   @param text
    #           Error text of the validation failure
    #
    #   @result
    #           False if self.raiseError is False, else raises a error of type self.errorClass.
    #
    def raiseFalse(self, text=""):
        if self.printError:
            print("EntityValidator.validate(...): Validation Failed >>>", text, "<<<")
        if self.raiseError:
            raise self.errorClass(text)
        return False

    #
    #   Desc:   Called if validation finished success.
    #
    #   @result
    #           True
    #
    def raiseTrue(self, text=""):
        return True


# Some predefined Validator that can be used imediately
entityValidatorThrowing = EntityValidator(
    raiseError=True, errorClass=InvalidInputError)
entityValidator = EntityValidator()
