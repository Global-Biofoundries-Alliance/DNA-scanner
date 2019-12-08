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
    def searchOffers(seqInf):
        raise NotImplementedError

    #
    #   Desc:   True if pinger is currently searching
    #
    def isRunning:
        raise NotImplementedError

    #
    #   Returns the current offers. Result can change while searching.
    #
    def getOffers:
        raise NotImplementedError

    #
    #
    #
    def registerVender(vendorInformation, vendorPinger):
        vendorHandler.append({ "vendor": vendorInformation, "handler": vendorPinger})

    def getVendors:
        result = []
        for vendor in vendorHandler:
            result.append(vendor.v)
        return result


class ProductivePinger(AbstractPinger):
        
    def __init__(self):
        print("productive pinger")

    def searchOffers(seqInf):
        pass

    def isRunning:
        return false

    def getOffers:
        return []


class DummyPinger(AbstractPinger):

    def __init__(self):
        raise NotImplementedError

    def searchOffers(seqInf):
        raise NotImplementedError

    def isRunning:
        return false

    def getOffers:
        return []
