import abc

class Message(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def addMessage(channel_id, author_id, message):
        pass
    
    @abc.abstractmethod
    def getAllMessage(channel_id, user_id):
        pass

    @abc.abstractmethod
    def getCountNotSeen(channel_id, user_id):
        pass

    @abc.abstractmethod
    def updateSeen(channel_id, user_id):
        pass

    @abc.abstractmethod
    def getLastTimeMessage(channel_id):
        pass

    @abc.abstractmethod
    def getAllUserNotSeen(channel_id):
        pass