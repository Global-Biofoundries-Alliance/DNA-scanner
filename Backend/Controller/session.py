#
#   A collection of classes related to session handling
#
from typing import List, Dict, Any

from Pinger.Entities import SequenceVendorOffers
from Pinger.Pinger import ManagedPinger



#
#   Desc:   Interface for handling of sessions.
#
class SessionManager:

    def __init__(self):
        self.sequences = []
        self.pinger = None
        self.filter = {}

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
    def loadSequences(self) -> List[SequenceVendorOffers]:
        raise NotImplementedError

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    def storeSequences(self, sequences: List[SequenceVendorOffers]) -> None:
        raise NotImplementedError

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> Dict[str, Any]:
        raise NotImplementedError

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: Dict[str, Any]) -> None:
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
    def storeSequences(self, sequences: List[SequenceVendorOffers]) -> None:
        self.sequences = sequences

    #
    #   Desc:   Loads the sequences out of the session-store.
    #
    def loadSequences(self) -> List[SequenceVendorOffers]:
        return self.sequences

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> Dict[str, Any]:
        return self.filter

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: Dict[str, Any]) -> None:
        self.filter = filter

    # TODO implement other functions

    def free(self):
        self.pinger = None


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
    def loadSequences(self) -> List[SequenceVendorOffers]:
        return self.session.loadSequences()

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    def storeSequences(self, sequences: List[SequenceVendorOffers]) -> None:
        self.session.storeSequences(sequences)

    #
    #   Desc: Loads the session's filter settings
    #
    def loadFilter(self) -> Dict[str, Any]:
        return self.session.loadFilter()

    #
    #   Desc: Stores filter settings in the session
    #
    def storeFilter(self, filter: Dict[str, Any]) -> None:
        self.session.storeFilter(filter)

    # TODO implement other functions

    def free(self):
        # TODO
        raise NotImplementedError
