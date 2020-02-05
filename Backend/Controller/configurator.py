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
        self.pinger = CompositePinger()
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

    #
    #   Gets the right pinger for a given pinger identifier.
    #   Put pinger specific initialization here.
    #
    #   @param id A valid pinger identifier
    #
    #   @result A pinger of type as specified by id and configured to the capacity of the config
    #
    def getPingerFromKey(self, id: str) -> BasePinger:
        cfg_pinger = self.cfg["pinger"]
        if id == "PINGER_TWIST":
            return BasePinger()
        if id == "PINGER_IDT":
            return BasePinger()
        if id == "PINGER_GENEART":
            return GeneArt(cfg_pinger["geneart"]["username"], cfg_pinger["geneart"]["token"]),
        if id == "PINGER_MOCK":
            return AdvancedMockPinger()
        else:
            #TODO Invalid-Contact-Your-Admin-Pinger here
            return None
