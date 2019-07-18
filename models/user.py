import abc

class User(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def addUser(username, password):
        pass

    @abc.abstractmethod
    def checkUser(username, password):
        pass
    
    @abc.abstractmethod
    def checkUserExist(username):
        pass

    @abc.abstractmethod
    def getUserIdByUsername(username):
        pass
    
    @abc.abstractmethod
    def addFriend(user_id, friend_id, status):
        pass

    @abc.abstractmethod
    def getFriendAllByStatus(user_id, status):
        pass

    @abc.abstractmethod
    def updateStatusFriend(user_id, friend_id, status):
        pass

    @abc.abstractmethod
    def removeFriend(user_id, friend_id):
        pass

    @abc.abstractmethod
    def getInfoUser(user_id):
        pass