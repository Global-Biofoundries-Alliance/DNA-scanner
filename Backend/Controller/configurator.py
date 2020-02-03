# python imports
import os

import yaml


# project imports
from Pinger.Pinger import BasePinger, CompositePinger
from Pinger.Entities import *
from Pinger.GeneArt import GeneArt
from Pinger.AdvancedMock import AdvancedMockPinger


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
        self.cfg = None

        if not os.path.isfile(filename):
            raise FileNotFoundError
        handle = open(filename, "r")
        self.cfg = yaml.safe_load(handle)
        handle.close()
        if "controller" not in self.cfg:
            raise KeyError
        cfg_controller = self.cfg["controller"]

        if "vendors" in cfg_controller:
            key = 0
            pingerIDTuples = []
            for vendor in cfg_controller["vendors"]:
                vendorInfo = VendorInformation(name=vendor["name"], shortName=vendor["shortName"], key=key)
                self.vendors.append({"name": vendor["name"], "shortName": vendor["shortName"], "key": key})
                pingerIDTuples.append((vendorInfo, vendor["pinger"]))
                key = key + 1
            self.initializePinger(pingerIDTuples)

    #
    #   see Configurator.initializePinger
    #
    #   @param pingers list of pinger configurations; Format: List(Tuple(VendorInformation, string))
    #                   where string is is a valid pinger identifier
    #
    def initializePinger(self, pingers=[]) -> None:
        for pingerInfo in pingers:
            newPinger = self.getPingerFromKey(pingerInfo[1])
            self.pinger.registerVendor(vendorInformation=pingerInfo[0], vendorPinger=newPinger)

    # Put pinger specific initialization here
    def getPingerFromKey(self, x) -> BasePinger:
        cfg_pinger = self.cfg["pinger"]
        if x == "PINGER_TWIST":
            return BasePinger()
        if x == "PINGER_IDT":
            return BasePinger()
        if x == "PINGER_GENEART":
            return GeneArt(cfg_pinger["geneart"]["username"], cfg_pinger["geneart"]["token"]),
        if x == "PINGER_MOCK":
            return AdvancedMockPinger()
        else:
            #TODO Invalid-Contact-Your-Admin-Pinger here
            return None
