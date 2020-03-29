#
#   A collection of classes related to session handling
#
from typing import List

from Pinger.Entities import SequenceInformation, SequenceVendorOffers, Message
from Pinger.Pinger import ManagedPinger
from Pinger.Validator import EntityValidator

validator = EntityValidator()

#
#   Desc:   Interface for handling of sessions.
#
class SessionManager:

    #
    #   Desc:   Loades the Pinger out of the session-store
    #
    #   @result
    #           Type ManagedPinger. 
    #
    def loadPinger(self) -> ManagedPinger:
        raise NotImplementedError

    # 
    #   Desc:   Stores the Pinger in the session-store
    #
    #   @param pinger
    #           Type ManagedPinger. The pinger to store.
    #
    def storePinger(self, pinger: ManagedPinger) -> None:
        raise NotImplementedError

    #
    #   Desc:   Loads the sequences out of the session-store.
    #
    def loadSequences(self) -> List[SequenceInformation]:
        raise NotImplementedError

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        raise NotImplementedError

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> dict:
        raise NotImplementedError

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: dict) -> None:
        raise NotImplementedError

    #
    #   Desc: Loads search results from the session
    #
    def loadResults(self) -> List[SequenceVendorOffers]:
        raise NotImplementedError

    #
    #   Desc: Stores a list of search results for later use
    #
    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        raise NotImplementedError

    #
    #   Desc: Adds a list of vendors that have already been searched
    #
    def addSearchedVendors(self, vendors: List[int]):
        raise NotImplementedError

    #
    #   Desc: Returns a list of vendors that have already been searched
    #
    def loadSearchedVendors(self) -> List[int]:
        raise NotImplementedError

    #
    #   Desc: Sets all vendors to not searched yet
    #
    def resetSearchedVendors(self):
        raise NotImplementedError

    #
    #   Desc: Adds a global message to this session
    #
    def addGlobalMessages(self, messages: List[Message]):
        raise NotImplementedError

    #
    #   Desc: Returns this session's global messages
    #
    def loadGlobalMessages(self) -> List[Message]:
        raise NotImplementedError

    #
    #   Desc: Deletes all global messages for this session
    #
    def clearGlobalMessages(self):
        raise NotImplementedError

    #
    #   Desc: Stores the current selection
    #
    def storeSelection(self, selection):
        raise NotImplementedError

    #
    #   Desc: Returns the current selection
    #
    def loadSelection(self):
        raise NotImplementedError

    #
    #   Desc: Sets the BOOST client
    #
    def storeBoostClient(self, boostClient):
        raise NotImplementedError

    #
    #   Desc: Returns the BOOST client
    #
    def loadBoostClient(self):
        raise NotImplementedError

    #
    #   Desc: Sets the host to be used for codon optimization
    #
    def storeHostOrganism(self, host: str):
        raise NotImplementedError

    #
    #   Desc: Returns the host to be used for codon optimization
    #
    def loadHostOrganism(self) -> str:
        raise NotImplementedError

    #
    #   Desc: Sets the juggling strategy used for codon optimization
    #
    def storeJugglingStrategy(self, strategy: str):
        raise NotImplementedError

    #
    #   Desc: Returns the juggling strategy used for codon optimization
    #
    def loadJugglingStrategy(self) -> str:
        raise NotImplementedError

    #
    #   Desc:   Free memory by Free all or old sessions. Can
    #           be different for every StoreManager.
    #
    def free(self):
        raise NotImplementedError


#
#   Representation of a single session.
#
class SingleSession(SessionManager):

    def __init__(self):
        self.sequences = []
        self.pinger = None
        self.filter = {}
        self.results = []
        self.searchedVendors = []
        self.globalMessages = []
        self.selection = []
        self.boostClient = None
        self.hostOrganism = ""
        self.jugglingStrategy = ""

    #
    #   Desc:   Loades the Pinger out of the session-store
    #
    #   @result
    #           Type ManagedPinger.
    #
    def loadPinger(self) -> ManagedPinger:
        return self.pinger

    #
    #   Desc:   Stores the Pinger in the session-store
    #
    #   @param pinger
    #           Type ManagedPinger. The pinger to store.
    #
    #   @raises TypeError if the object to store is of the wrong type
    #
    def storePinger(self, pinger: ManagedPinger) -> None:
        if not isinstance(pinger, ManagedPinger):
            raise TypeError
        self.pinger = pinger

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    #   @raises TypeError if there is a malformed sequence in the list
    #
    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        for seq in sequences:
            if not isinstance(seq, SequenceInformation):
                raise TypeError
        if not validator.validate(sequences):
            raise TypeError
        self.sequences = sequences

    #
    #   Desc:   Loads the sequences out of the session-store.
    #
    def loadSequences(self) -> List[SequenceInformation]:
        return self.sequences

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: dict) -> None:
        self.filter = filter

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> dict:
        return self.filter

    #
    #   Desc: Loads search results from the session
    #
    def loadResults(self) -> List[SequenceVendorOffers]:
        return self.results

    #
    #   Desc: Stores a list of search results for later use
    #
    #   @raises TypeError if one the objects to store is of the wrong type
    #
    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        for res in results:
            if not isinstance(res, SequenceVendorOffers):
                raise TypeError
        if not validator.validate(results):
            raise TypeError
        self.results = results

    #
    #   Desc: Adds a list of vendors that have already been searched
    #
    #   @raises TypeError if one of the vendor IDs is not int
    #
    def addSearchedVendors(self, vendors: List[int]):
        for vendor in vendors:
            if not isinstance(vendor, int):
                raise TypeError
        self.searchedVendors.extend(vendors)

    #
    #   Desc: Returns a list of vendors that have already been searched
    #
    def loadSearchedVendors(self) -> List[int]:
        return self.searchedVendors

    #
    #   Desc: Sets all vendors to not searched yet
    #
    def resetSearchedVendors(self):
        self.searchedVendors = []

    #
    #   Desc: Adds a global message to this session
    #
    def addGlobalMessages(self, messages: List[Message]):
        self.globalMessages.extend(messages)

    #
    #   Desc: Returns this session's global messages
    #
    def loadGlobalMessages(self) -> List[Message]:
        return self.globalMessages

    #
    #   Desc: Deletes all global messages for this session
    #
    def clearGlobalMessages(self):
        self.globalMessages = []

    #
    #   Desc: Stores the current selection
    #
    def storeSelection(self, selection):
        self.selection = selection

    #
    #   Desc: Returns the current selection
    #
    def loadSelection(self):
        return self.selection

    #
    #   Desc: Sets the BOOST client
    #
    def storeBoostClient(self, boostClient):
        self.boostClient = boostClient

    #
    #   Desc: Returns the BOOST client
    #
    def loadBoostClient(self):
        return self.boostClient

    #
    #   Desc: Sets the host to be used for codon optimization
    #
    def storeHostOrganism(self, host: str):
        self.hostOrganism = host

    #
    #   Desc: Returns the host to be used for codon optimization
    #
    def loadHostOrganism(self) -> str:
        return self.hostOrganism

    #
    #   Desc: Sets the juggling strategy used for codon optimization
    #
    def storeJugglingStrategy(self, strategy: str):
        self.jugglingStrategy = strategy

    #
    #   Desc: Returns the juggling strategy used for codon optimization
    #
    def loadJugglingStrategy(self) -> str:
        return self.jugglingStrategy

    def free(self):
        self.sequences = []
        self.pinger = None
        self.filter = {}
        self.results = []


class InMemorySessionManager(SessionManager):
    sessions = []

    def __init__(self, sessionId):
        self.session = None

        for (sid, sm) in InMemorySessionManager.sessions:
            if (sid == sessionId):
                self.session = sm

        if (self.session == None):
            self.session = SingleSession()
            InMemorySessionManager.sessions.append((sessionId, self.session))

    #
    #   Desc: Returns whether a session ID is already present
    #
    #   @param id
    #       The session ID to check for
    #
    #   @result
    #       True if the ID is already taken, False otherwise
    #
    @staticmethod
    def hasSession(id):
        for (sid, sm) in InMemorySessionManager.sessions:
            if sid == id:
                return True
        return False

    #
    #   Desc:   Loades the Pinger out of the session-store
    #
    #   @result
    #           Type ManagedPinger.
    #
    def loadPinger(self) -> ManagedPinger:
        return self.session.loadPinger()

    #
    #   Desc:   Stores the Pinger in the session-store
    #
    #   @param pinger
    #           Type ManagedPinger. The pinger to store.
    #
    def storePinger(self, pinger: ManagedPinger) -> None:
        return self.session.storePinger(pinger)

    #
    #   Desc:   Loads the sequences out of the session-store.
    #
    def loadSequences(self) -> List[SequenceInformation]:
        return self.session.loadSequences()

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        self.session.storeSequences(sequences)

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> dict:
        return self.session.loadFilter()

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: dict) -> None:
        self.session.storeFilter(filter)

    #
    #   Desc: Loads search results from the session
    #
    def loadResults(self) -> List[SequenceVendorOffers]:
        return self.session.loadResults()

    #
    #   Desc: Stores a list of search results for later use
    #
    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        self.session.storeResults(results)

    #
    #   Desc: Adds a list of vendors that have already been searched
    #
    def addSearchedVendors(self, vendors: List[int]):
        self.session.addSearchedVendors(vendors)

    #
    #   Desc: Returns a list of vendors that have already been searched
    #
    def loadSearchedVendors(self) -> List[int]:
        return self.session.loadSearchedVendors()

    #
    #   Desc: Sets all vendors to not searched yet
    #
    def resetSearchedVendors(self):
        self.session.resetSearchedVendors()

    #
    #   Desc: Adds a global message to this session
    #
    def addGlobalMessages(self, messages: List[Message]):
        self.session.addGlobalMessages(messages)

    #
    #   Desc: Returns this session's global messages
    #
    def loadGlobalMessages(self) -> List[Message]:
        return self.session.loadGlobalMessages()

    #
    #   Desc: Deletes all global messages for this session
    #
    def clearGlobalMessages(self):
        self.session.clearGlobalMessages()

    #
    #   Desc: Stores the current selection
    #
    def storeSelection(self, selection):
        self.session.storeSelection(selection)

    #
    #   Desc: Returns the current selection
    #
    def loadSelection(self):
        return self.session.loadSelection()

    #
    #   Desc: Sets the BOOST client
    #
    def storeBoostClient(self, boostClient):
        self.session.storeBoostClient(boostClient)

    #
    #   Desc: Returns the BOOST client
    #
    def loadBoostClient(self):
        return self.session.loadBoostClient()

    #
    #   Desc: Sets the host to be used for codon optimization
    #
    def storeHostOrganism(self, host: str):
        self.session.storeHostOrganism(host)

    #
    #   Desc: Returns the host to be used for codon optimization
    #
    def loadHostOrganism(self) -> str:
        return self.session.loadHostOrganism()

    #
    #   Desc: Sets the juggling strategy used for codon optimization
    #
    def storeJugglingStrategy(self, strategy: str):
        self.session.storeJugglingStrategy(strategy)

    #
    #   Desc: Returns the juggling strategy used for codon optimization
    #
    def loadJugglingStrategy(self) -> str:
        return self.session.loadJugglingStrategy()


    #
    #   Desc: Frees all sessions
    #
    def free(self):
        for (sid, sm) in InMemorySessionManager.sessions:
            sm.free()
        InMemorySessionManager.sessions = []
