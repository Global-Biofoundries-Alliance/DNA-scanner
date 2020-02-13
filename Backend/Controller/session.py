#
#   A collection of classes related to session handling
#
from typing import List, Dict, Any

from Pinger.Entities import SequenceInformation, SequenceVendorOffers
from Pinger.Pinger import ManagedPinger



#
#   Desc:   Interface for handling of sessions.
#
class SessionManager:

    def __init__(self):
        self.sequences = []
        self.pinger = None
        self.filter = {}
        self.results = []
        self.searchedVendors = []

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
    def storePinger(self, pinger: ManagedPinger) -> None:
        self.pinger = pinger

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        self.sequences = sequences

    #
    #   Desc:   Loads the sequences out of the session-store.
    #
    def loadSequences(self) -> List[SequenceInformation]:
        return self.sequences

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> dict:
        return self.filter

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: dict) -> None:
        self.filter = filter

    #
    #   Desc: Loads search results from the session
    #
    def loadResults(self) -> List[SequenceVendorOffers]:
        return self.results

    #
    #   Desc: Stores a list of search results for later use
    #
    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        self.results = results

    #
    #   Desc: Adds a list of vendors that have already been searched
    #
    def addSearchedVendors(self, vendors: List[int]):
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
    #   Desc: Frees all sessions
    #
    def free(self):
        for session in self.sessions:
            session.free()
        sessions = []
