'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
from typing import List

from Pinger.Entities import SequenceInformation, SequenceVendorOffers, Message
from Pinger.Pinger import ManagedPinger
from Pinger.Validator import EntityValidator


validator = EntityValidator()

#
#   A collection of classes related to session handling
#


class SessionManager:
    '''Interface for handling of sessions.'''

    def loadPinger(self) -> ManagedPinger:
        '''
        Loades the Pinger out of the session-store

        @result
            Type ManagedPinger.
        '''
        raise NotImplementedError

    def storePinger(self, pinger: ManagedPinger) -> None:
        '''
        Stores the Pinger in the session-store

        @param pinger
            Type ManagedPinger. The pinger to store.
        '''
        raise NotImplementedError

    def loadSequences(self) -> List[SequenceInformation]:
        '''Loads the sequences out of the session-store.'''
        raise NotImplementedError

    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        '''Loads the sequences out of the session-store.'''
        raise NotImplementedError

    def loadFilter(self) -> dict:
        '''Loads the session's fltr settings.'''
        raise NotImplementedError

    def storeFilter(self, fltr: dict) -> None:
        '''Stores fltr settings in the session.'''
        raise NotImplementedError

    def loadResults(self) -> List[SequenceVendorOffers]:
        '''Loads search results from the session.'''
        raise NotImplementedError

    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        '''Stores a list of search results for later use.'''
        raise NotImplementedError

    def addSearchedVendors(self, vendors: List[int]):
        '''Adds a list of vendors that have already been searched.'''
        raise NotImplementedError

    def loadSearchedVendors(self) -> List[int]:
        '''Returns a list of vendors that have already been searched.'''
        raise NotImplementedError

    def resetSearchedVendors(self):
        '''Sets all vendors to not searched yet.'''
        raise NotImplementedError

    def addGlobalMessages(self, messages: List[Message]):
        '''Adds a global message to this session.'''
        raise NotImplementedError

    def loadGlobalMessages(self) -> List[Message]:
        '''Returns this session's global messages.'''
        raise NotImplementedError

    def loadVendorMessages(self):
        '''Store per vendor messages as a dictionary of the form
        {key: [<messages>]} where key is the vendor key.'''
        raise NotImplementedError

    def storeVendorMessages(self, vendorMessages):
        '''Returns per vendor messages as a dictionary of the form
        {key: [<messages>]} where key is the vendor key.'''
        raise NotImplementedError

    def clearGlobalMessages(self):
        '''Deletes all global messages for this session.'''
        raise NotImplementedError

    def storeSelection(self, selection):
        '''Stores the current selection.'''
        raise NotImplementedError

    def loadSelection(self):
        '''Returns the current selection.'''
        raise NotImplementedError

    def storeBoostClient(self, boostClient):
        '''Sets the BOOST client.'''
        raise NotImplementedError

    def loadBoostClient(self):
        '''Returns the BOOST client.'''
        raise NotImplementedError

    def storeHostOrganism(self, host: str):
        '''Sets the host to be used for codon optimization.'''
        raise NotImplementedError

    def loadHostOrganism(self) -> str:
        '''Returns the host to be used for codon optimization.'''
        raise NotImplementedError

    def storeJugglingStrategy(self, strategy: str):
        '''Sets the juggling strategy used for codon optimization.'''
        raise NotImplementedError

    def loadJugglingStrategy(self) -> str:
        '''Returns the juggling strategy used for codon optimization.'''
        raise NotImplementedError

    def free(self):
        '''Free memory by Free all or old sessions. Can be different for
        every StoreManager.'''
        raise NotImplementedError


class SingleSession(SessionManager):
    '''Representation of a single session.'''

    def __init__(self):
        self.sequences = []
        self.pinger = None
        self.fltr = {}
        self.results = []
        self.searchedVendors = []
        self.globalMessages = []
        self.vendorMessages = {}
        self.selection = []
        self.boostClient = None
        self.hostOrganism = ""
        self.jugglingStrategy = ""

    def loadPinger(self) -> ManagedPinger:
        '''
        Loades the Pinger out of the session-store

        @result
            Type ManagedPinger.
        '''
        return self.pinger

    def storePinger(self, pinger: ManagedPinger) -> None:
        '''
        Stores the Pinger in the session-store

        @param pinger
            Type ManagedPinger. The pinger to store.

        @raises TypeError if the object to store is of the wrong type
        '''
        if not isinstance(pinger, ManagedPinger):
            raise TypeError
        self.pinger = pinger

    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        '''
        Loads the sequences out of the session-store

        @raises TypeError if there is a malformed sequence in the list
        '''
        for seq in sequences:
            if not isinstance(seq, SequenceInformation):
                raise TypeError
        if not validator.validate(sequences):
            raise TypeError
        self.sequences = sequences

    def loadSequences(self) -> List[SequenceInformation]:
        '''Loads the sequences out of the session-store.'''
        return self.sequences

    def storeFilter(self, fltr: dict) -> None:
        '''Stores fltr settings in the session.'''
        self.fltr = fltr

    def loadFilter(self) -> dict:
        '''Loads the session's fltr settings.'''
        return self.fltr

    def loadResults(self) -> List[SequenceVendorOffers]:
        '''Loads search results from the session.'''
        return self.results

    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        '''
        Stores a list of search results for later use

        @raises TypeError if one the objects to store is of the wrong type.
        '''
        for res in results:
            if not isinstance(res, SequenceVendorOffers):
                raise TypeError
        if not validator.validate(results):
            raise TypeError
        self.results = results

    def addSearchedVendors(self, vendors: List[int]):
        '''
        Adds a list of vendors that have already been searched

        @raises TypeError if one of the vendor IDs is not int
        '''
        for vendor in vendors:
            if not isinstance(vendor, int):
                raise TypeError
        self.searchedVendors.extend(vendors)

    def loadSearchedVendors(self) -> List[int]:
        '''Returns a list of vendors that have already been searched.'''
        return self.searchedVendors

    def resetSearchedVendors(self):
        '''Sets all vendors to not searched yet.'''
        self.searchedVendors = []

    def addGlobalMessages(self, messages: List[Message]):
        '''Adds a global message to this session.'''
        # Add messages unless they are already present
        for message in messages:
            if message not in self.globalMessages:
                self.globalMessages.append(message)

    def loadGlobalMessages(self) -> List[Message]:
        '''Returns this session's global messages.'''
        return self.globalMessages

    def clearGlobalMessages(self):
        '''Deletes all global messages for this session.'''
        self.globalMessages = []

    def loadVendorMessages(self):
        '''Store per vendor messages as a dictionary of the form
        {key: [<messages>]} where key is the vendor key.'''
        return self.vendorMessages

    def storeVendorMessages(self, vendorMessages):
        '''Returns per vendor messages as a dictionary of the form
        {key: [<messages>]} where key is the vendor key.'''
        self.vendorMessages = vendorMessages

    def storeSelection(self, selection):
        '''Stores the current selection.'''
        self.selection = selection

    def loadSelection(self):
        '''Returns the current selection.'''
        return self.selection

    def storeBoostClient(self, boostClient):
        '''Sets the BOOST client.'''
        self.boostClient = boostClient

    def loadBoostClient(self):
        '''Returns the BOOST client.'''
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
        self.fltr = {}
        self.results = []


class InMemorySessionManager(SessionManager):
    '''InMemorySessionManager.'''
    sessions = []

    def __init__(self, sessionId):
        self.session = None

        for (sid, sm) in InMemorySessionManager.sessions:
            if sid == sessionId:
                self.session = sm

        if self.session is None:
            self.session = SingleSession()
            InMemorySessionManager.sessions.append((sessionId, self.session))

    @staticmethod
    def hasSession(session_id):
        '''
        Returns whether a session ID is already present

        @param session_id
            The session ID to check for

        @result
            True if the ID is already taken, False otherwise
        '''
        for (sid, _) in InMemorySessionManager.sessions:
            if sid == session_id:
                return True
        return False

    def loadPinger(self) -> ManagedPinger:
        '''
        Loades the Pinger out of the session-store

        @result
            Type ManagedPinger.
        '''
        return self.session.loadPinger()

    def storePinger(self, pinger: ManagedPinger) -> None:
        '''
        Stores the Pinger in the session-store

        @param pinger
            Type ManagedPinger. The pinger to store.
        '''
        return self.session.storePinger(pinger)

    def loadSequences(self) -> List[SequenceInformation]:
        '''Loads the sequences out of the session-store.'''
        return self.session.loadSequences()

    def storeSequences(self, sequences: List[SequenceInformation]) -> None:
        '''Loads the sequences out of the session-store.'''
        self.session.storeSequences(sequences)

    def loadFilter(self) -> dict:
        '''Loads the session's fltr settings.'''
        return self.session.loadFilter()

    def storeFilter(self, fltr: dict) -> None:
        '''Stores fltr settings in the session.'''
        self.session.storeFilter(fltr)

    def loadResults(self) -> List[SequenceVendorOffers]:
        '''Loads search results from the session.'''
        return self.session.loadResults()

    def storeResults(self, results: List[SequenceVendorOffers]) -> None:
        '''Stores a list of search results for later use.'''
        self.session.storeResults(results)

    def addSearchedVendors(self, vendors: List[int]):
        '''Adds a list of vendors that have already been searched.'''
        self.session.addSearchedVendors(vendors)

    def loadSearchedVendors(self) -> List[int]:
        '''Returns a list of vendors that have already been searched.'''
        return self.session.loadSearchedVendors()

    def resetSearchedVendors(self):
        '''Sets all vendors to not searched yet.'''
        self.session.resetSearchedVendors()

    def addGlobalMessages(self, messages: List[Message]):
        '''Adds a global message to this session.'''
        self.session.addGlobalMessages(messages)

    def loadGlobalMessages(self) -> List[Message]:
        '''Returns this session's global messages.'''
        return self.session.loadGlobalMessages()

    def clearGlobalMessages(self):
        '''Deletes all global messages for this session.'''
        self.session.clearGlobalMessages()

    def loadVendorMessages(self):
        '''Store per vendor messages as a dictionary of the form
        {key: [<messages>]} where key is the vendor key.'''
        return self.session.loadVendorMessages()

    def storeVendorMessages(self, vendorMessages):
        '''Returns per vendor messages as a dictionary of the form
        {key: [<messages>]} where key is the vendor key.'''
        self.session.storeVendorMessages(vendorMessages)

    def storeSelection(self, selection):
        '''Stores the current selection.'''
        self.session.storeSelection(selection)

    def loadSelection(self):
        '''Returns the current selection.'''
        return self.session.loadSelection()

    def storeBoostClient(self, boostClient):
        '''Sets the BOOST client.'''
        self.session.storeBoostClient(boostClient)

    def loadBoostClient(self):
        '''Returns the BOOST client.'''
        return self.session.loadBoostClient()

    def storeHostOrganism(self, host: str):
        '''Sets the host to be used for codon optimization.'''
        self.session.storeHostOrganism(host)

    def loadHostOrganism(self) -> str:
        '''Returns the host to be used for codon optimization.'''
        return self.session.loadHostOrganism()

    def storeJugglingStrategy(self, strategy: str):
        '''Sets the juggling strategy used for codon optimization.'''
        self.session.storeJugglingStrategy(strategy)

    def loadJugglingStrategy(self) -> str:
        '''Returns the juggling strategy used for codon optimization.'''
        return self.session.loadJugglingStrategy()

    def free(self):
        '''Frees all sessions.'''
        for (_, sm) in InMemorySessionManager.sessions:
            sm.free()
        InMemorySessionManager.sessions = []
