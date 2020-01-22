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

from Pinger.Entities import *

class Validator:
    def __init__(self):
        raise NotImplementedError

    def validate(self, obj):
        raise NotImplementedError

class EntityValidator:
    def __init__(self):
        pass

    def validate(self, obj):
        if isinstance(obj, VendorInformation):
            if(not isinstance(obj.key, int)):
                return self.raiseFalse("key is not a numeric value")
            if(not isinstance(obj.shortName, str)):
                return self.raiseFalse("shortName is not a String")
            if(not isinstance(obj.name, str)):
                return self.raiseFalse("name is not a String")

        else:
            return self.raiseFalse("The object to validate has a not supported type")

        return self.raiseTrue()

    def raiseFalse(self, text = ""):
        print("Validation Failed:", text)
        return False

    def raiseTrue(self, text = ""):
        return True

entityValidator = EntityValidator()
