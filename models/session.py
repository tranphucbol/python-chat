import abc

class Session(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def addSession(user_id, session_id):
        pass
    
    @abc.abstractmethod
    def checkUserOnline(user_id):
        pass

    @abc.abstractmethod
    def updateSession(user_id, session_id):
        pass
    
    @abc.abstractmethod
    def removeSession(session_id):
        pass

    @abc.abstractmethod
    def checkSession(session_id):
        pass