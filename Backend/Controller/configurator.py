# python imports

import yaml
from Pinger.AdvancedMock import AdvancedMockPinger
from Pinger.Entities import *
from Pinger.GeneArt import GeneArt
# project imports
from Pinger.Pinger import BasePinger, ManagedPinger, CompositePinger


#
#   Desc:   Interface for configuration-objects. These objects 
#           are managing all values of the controller, that can be stored 
#           outside in a configuration-file.
#
class Configurator:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Initialize the Pinger.
    #
    #   @result
    #           Returns a managedPinger with registered BasePingers.
    #
    def initializePinger(self) -> ManagedPinger:
        raise NotImplementedError


#
#   Desc:   Takes a yaml-file with all configuration-properties
#
class YmlConfigurator(Configurator):

    #
    #   Desc:   Constructor
    #
    #   @param filename
    #           Type String. Specifies the file with the configuration 
    #           properties.
    #
    #   @throws IOError
    #           if the file could not be opened
    #
    #   @throws KeyError
    #           if there is a required configuration item missing
    #
    #   @throws YAMLError
    #           if the YAML file is invalid
    def __init__(self, filename) -> None:
        self.vendors = []
        self.cfg = None

        # Acquire config from YAML file
        handle = open(filename, "r")
        self.cfg = yaml.safe_load(handle)
        handle.close()

        cfg_controller = self.cfg["controller"]

        if "vendors" in cfg_controller:
            key = 0
            pingerIDTuples = []
            for vendor in cfg_controller["vendors"]:
                vendorInfo = VendorInformation(name=vendor["name"], shortName=vendor["shortName"], key=key)
                self.vendors.append(vendorInfo)
                pingerIDTuples.append((vendorInfo, vendor["pinger"]))
                key = key + 1

    #
    #   see Configurator.initializePinger
    #
    def initializePinger(self) -> ManagedPinger:
        cfg_controller = self.cfg["controller"]
        pinger = CompositePinger()
        pingerIDTuples = []
        key = 0
        for vendor in cfg_controller["vendors"]:
            vendorInfo = VendorInformation(name=vendor["name"], shortName=vendor["shortName"], key=key)
            pingerIDTuples.append((vendorInfo, vendor["pinger"]))
            key = key + 1

        for pingerInfo in pingerIDTuples:
            newPinger = self.getPingerFromKey(pingerInfo[1])
            pinger.registerVendor(vendorInformation=pingerInfo[0], vendorPinger=newPinger)
        return pinger

    #
    #   Gets the right pinger for a given pinger identifier.
    #   Put pinger specific initialization here.
    #
    #   @param id A valid pinger identifier
    #
    #   @result A pinger of type as specified by id and configured to the capacity of the config
    #
    def getPingerFromKey(self, id: str) -> BasePinger:
        try:
            cfg_pinger = self.cfg["pinger"]
            if id == "PINGER_TWIST":
                return BasePinger()
            if id == "PINGER_IDT":
                return BasePinger()
            if id == "PINGER_GENEART":
                cfg_geneart = cfg_pinger["geneart"]
                return GeneArt(username=cfg_geneart["username"],
                               token=cfg_geneart["token"],
                               server=cfg_geneart["server"],
                               validate=cfg_geneart["validate"],
                               status=cfg_geneart["status"],
                               addToCart=cfg_geneart["addToCart"],
                               upload=cfg_geneart["upload"],
                               dnaStrings=cfg_geneart["dnaStrings"],
                               hqDnaStrings=cfg_geneart["hqDnaStrings"],
                               timeout=cfg_geneart["timeout"])
            if id == "PINGER_MOCK":
                return AdvancedMockPinger()
            else:
                # TODO Invalid-Contact-Your-Admin-Pinger here
                return None
        except:
            # TODO Invalid-Contact-Your-Admin-Pinger here
            return None