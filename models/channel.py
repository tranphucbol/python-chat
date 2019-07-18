import abc

class Channel(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def createChannel():
        pass

    @abc.abstractmethod
    def addUserToChannel(channel_id, user_id):
        pass

    @abc.abstractmethod
    def getAllChannelTwoUser(user_id):
        pass

    @abc.abstractmethod
    def getAllChannel(user_id):
        pass
    
    @abc.abstractmethod
    def getChannelName(channel_id, user_id=None):
        pass