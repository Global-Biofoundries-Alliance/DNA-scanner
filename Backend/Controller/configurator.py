# python imports
import yaml
import os

# project imports
from Pinger.Pinger import BasePinger, CompositePinger
from Pinger.AdvancedMock import AdvancedMockPinger
from Pinger.GeneArt import GeneArt
from Pinger.Entities import *


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
    def initializePinger(self):
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
    #   @throws FileNotFoundError 
    #           if file from parameter filename is not found
    #
    #   @throws KeyError
    #           if there is no configuration for the controller present
    #
    #   @throws YAMLError
    #           if the YAML file is invalid
    def __init__(self, filename) -> None:
        self.vendors = []
        self.pinger = CompositePinger()

        if not os.path.isfile(filename):
            raise FileNotFoundError

        all_cfg = yaml.safe_load(open(filename, "r"))
        if "controller" not in all_cfg:
            raise KeyError
        cfg = all_cfg["controller"]

        if "vendors" in cfg:
            key = 0
            pingerIDTuples = []
            for vendor in cfg["vendors"]:
                vendorInfo = VendorInformation(name=vendor["name"], shortName=vendor["shortName"], key=key)
                self.vendors.append(vendorInfo)
                pingerIDTuples.append((vendorInfo, vendor["pinger"]))
                key = key + 1

    #
    #   see Configurator.initializePinger
    #
    #   @param pingers list of pinger configurations; Format: List(Tuple(VendorInformation, string))
    #                   where string is is a valid pinger identifier
    #
    def initializePinger(self, pingers=[]) -> None:
        for pingerInfo in pingers:
            newPinger = self.getPingerFromKey(pingerInfo[1])
            if newPinger:
                self.pinger.registerVendor(pingerInfo[0], newPinger)

        # TODO implement
        raise NotImplementedError

    def getPingerFromKey(x):
        return {
            "PINGER_TWIST":
                BasePinger(),
            "PINGER_IDT":
                BasePinger(),
            "PINGER_GENEART":
                BasePinger(),
            "PINGER_MOCK":
                AdvancedMockPinger()
        }.get(x, None)
