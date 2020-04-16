import yaml
from Pinger.AdvancedMock import AdvancedMockPinger
from Pinger.Entities import *
from Pinger.GeneArt import GeneArt
from Pinger.IDT import IDT
from Pinger.Twist import Twist
from .parser import BoostClient
from .session import SessionManager
import traceback

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
    def initializePinger(self, session: SessionManager) -> ManagedPinger:
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

        # Initialize static vendor list and assign IDs.
        if "vendors" in cfg_controller:
            key = 0
            for vendor in cfg_controller["vendors"]:
                vendorInfo = VendorInformation(name=vendor["name"], shortName=vendor["shortName"], key=key)
                self.vendors.append(vendorInfo)
                key = key + 1

    #
    #   see Configurator.initializePinger
    #
    def initializePinger(self, session: SessionManager) -> ManagedPinger:
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
            # Catch pingers that could not be initialized for any reason
            if isinstance(newPinger, Message):
                session.addGlobalMessages([newPinger])
                continue
            if isinstance(newPinger, AdvancedMockPinger):
                session.addGlobalMessages(["Warning: A mock vendor is being used. Contact an administrator."])
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
                cfg_twist = cfg_pinger["twist"]
                return Twist(cfg_twist["email"],
                             cfg_twist["password"],
                             cfg_twist["apitoken"],
                             cfg_twist["eutoken"],
                             cfg_twist["username"],
                             cfg_twist["firstname"],
                             cfg_twist["lastname"],
                             host=cfg_twist["server"])
            if id == "PINGER_IDT":
                cfg_idt = cfg_pinger["idt"]
                pinger = IDT(idt_username=cfg_idt["username"],
                             idt_password=cfg_idt["password"],
                             client_id=cfg_idt["client_id"],
                             client_secret=cfg_idt["client_secret"],
                             shared_secret=cfg_idt["shared_secret"],
                             scope=cfg_idt["scope"])
                token = pinger.getToken()
                # This may return a message instead of a token in case of failure
                if isinstance(token, Message):
                    return token
                else:
                    pinger.token = token
                return pinger

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
                return InvalidPinger()
        except:
            return InvalidPinger()

    def initializeBoostClient(self):
        try:
            cfg_boost = self.cfg["boost"]
            return BoostClient(url_job=cfg_boost["url_job"],
                               url_hosts=cfg_boost["url_hosts"],
                               url_submit=cfg_boost["url_submit"],
                               url_login=cfg_boost["url_login"],
                               username=cfg_boost["username"],
                               password=cfg_boost["password"],
                               timeout=cfg_boost["timeout"])
        except Exception as error:
            print(traceback.format_exc())
            return None


#
#   The InvalidPinger is used if a pinger could not be initialized due to a misconfiguration.
#   Its purpose is to tell the user to contact the system's admin.
#
class InvalidPinger(BasePinger):

    def __init__(self):
        self.tempOffer = Offer(price=Price(currency=Currency.EUR, amount=-1), turnovertime=-1)
        self.tempOffer.messages.append(
            Message(MessageType.WRONG_CREDENTIALS, "Invalid vendor configuration. Please contact your administrator."))
        self.offers = []
        self.vendorMessages = [Message(MessageType.VENDOR_INFO, "Invalid vendor configuration. Please contact your administrator.")]
        self.running = False

    #
    #   After:
    #       isRunning() -> true
    #       getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer), SequenceOffer(seqInf[1], self.tempOffer), ...
    #                           SequenceOffer(seqInf[n], self.tempOffer)]
    #
    def searchOffers(self, seqInf):
        self.running = True
        self.offers = []
        for s in seqInf:
            self.offers.append(SequenceOffers(sequenceInformation=s, offers=[self.tempOffer]))
        self.running = False

    #
    #   True if searchOffers called last
    #   False if getOffers called last
    #
    def isRunning(self):
        return self.running

    #
    #   Returns List with a  SequenceOffer for every sequence in last searchOffers(seqInf)-call.
    #   Every SequenceOffer contains the same offers. Default 1 see self.tempOffer and self.offers.
    #
    def getOffers(self):
        return self.offers

    def clear(self):
        self.offers = []
        self.vendorMessages = [Message(MessageType.VENDOR_INFO, "Invalid vendor configuration. Please contact your administrator.")]
        self.running = False

    def order(self, offerIds):
        return Order(OrderType.NOT_SUPPORTED)

    def getVendorMessages(self):
        return self.vendorMessages

    #
    #   Desc:   Adds a vendor message to this vendor's message store.
    #
    #   @result
    #           Type Message
    #           The message to be added
    #
    def addVendorMessage(self, message):
        self.vendorMessages.append(message)