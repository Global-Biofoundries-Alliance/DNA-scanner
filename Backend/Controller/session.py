#
#   Desc:   Interface for handling of sessions.
#
class SessionManager:

    def __init__(self):
        raise NotImplementedError

    #
    #   Desc:   Loades the Pinger out of the session-store
    #
    #   @result
    #           Type ManagedPinger. 
    #
    def loadPinger(self):
        raise NotImplementedError

    # 
    #   Desc:   Stores the Pinger in the session-store
    #
    #   @param pinger
    #           Type ManagedPinger. The pinger to store.
    #
    def storePinger(self, pinger):
        raise NotImplementedError

    #
    #   Desc:   Loads the sequences out of the session-store.
    #
    #   @result
    #           TODO Type
    #
    def loadSequences(self):
        raise NotImplementedError

    #
    #   Desc:   Loads the sequences out of the session-store
    #
    #   @result
    #           TODO Type
    #
    def storeSeqquences(self, sequences):
        raise NotImplementedError

    #
    #   Desc:   Free memmory by Free all or old sessions. Can
    #           be different for every StoreManager.
    #
    def free(self):
        raise NotImplementedError

#
#   Representation of a single session.
#
class SingleSession(SessionManager):

    def __init__(self):
        self.pinger = None
        pass

    def loadPinger(self):
        return self.pinger

    def storePinger(self, pinger):
        self.pinger = pinger

    # TODO implemented other functions

    def free(self):
        self.pinger = None


class InMemmorySessionManager(SessionManager):

    sessions = []

    def __init__(self, sessionId):
        self.session = None

        for (sid, sm) in DefaultSessionManager.sessions:
            if(sid == sessionId):
                self.session = sm

        if (self.session == None):
            self.session = SingleSession()
            DefaultSessionManager.sessions.append( (sessionId, self.session) )

    def loadPinger(self):
        return self.session.loadPinger()

    def storePinger(self, pinger)
        return self.session.storePinger()

    # TODO implement other functions

    def free():
        # TODO
        raise NotImplementedError


