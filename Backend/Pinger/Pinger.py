#########################################################
#                                                       #
#   Pinger                                              #
#                                                       #
#########################################################

vendors = [
#    VendorInformation("geneart", " GeneArt AG", "GeneArt")
]


class AbstractPinger:

    vendorHandler = []

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Start a search for the given sequence. 
    #           Has no result, because asynchronous search.
    #
    def searchOffers(self, seqInf):
        raise NotImplementedError

    #
    #   Desc:   True if pinger is currently searching
    #
    def isRunning(self):
        raise NotImplementedError

    #
    #   Returns the current offers. Result can change while searching.
    #
    def getOffers(self):
        raise NotImplementedError

    #
    #
    #
    def registerVender(self, vendorInformation, vendorPinger):
        self.vendorHandler.append({ "vendor": vendorInformation, "handler": vendorPinger})

    def getVendors(self):
        result = []
        for vendor in self.vendorHandler:
            result.append(vendor.v)
        return result


class ProductivePinger(AbstractPinger):
        
    def __init__(self):
        print("productive pinger")

    def searchOffers(self, seqInf):
        pass

    def isRunning(self):
        return False

    def getOffers(self):
        return []


class DummyPinger(AbstractPinger):

    def __init__(self):
        raise NotImplementedError

    def searchOffers(seqInf):
        raise NotImplementedError

    def isRunning(self):
        return False

    def getOffers(self):
        return []
