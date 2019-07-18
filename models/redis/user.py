import connectRedis as connect
import uuid
import bcrypt
import datetime
from models.user import User as UserInterface

class User(UserInterface):
    def addUser(self, username, password):
        r = connect.createConnect()
        user_id = str(uuid.uuid1())
        data = {
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            'user_id': user_id
        }
        r.hmset('users:{}'.format(username), data)
        r.hmset('user_infos:{}'.format(user_id), {'username': username})

    def checkUser(self, username, password):
        r = connect.createConnect()
        pw = r.hget('users:{}'.format(username), 'password').decode('utf-8')
        if pw != None and bcrypt.checkpw(password.encode('utf-8'), pw.encode('utf-8')):
            return True
        return False

    def getUserIdByUsername(self, username):
        r = connect.createConnect()
        data = r.hget('users:{}'.format(username), 'user_id')
        return data.decode('utf-8')

    def checkUserExist(self, username):
        r = connect.createConnect()
        return True if r.exists('users:{}'.format(username)) == 1 else False
    
    def addFriend(self, user_id, friend_id, status):
        r = connect.createConnect()
        r.hmset('friend:{}:{}'.format(user_id, friend_id), {'status': 1})

    def getFriendAllByStatus(self, user_id, status):
        r = connect.createConnect()
        keys = r.keys('friend:{}:*'.format(user_id))
        friends = []
        for key in keys:
            friends.append({
                'status': r.hget(key, 'status').decode('utf-8')
            })

        return friends

    def updateStatusFriend(self, user_id, friend_id, status):
        pass

    def removeFriend(self, user_id, friend_id):
        pass

    def getInfoUser(self, user_id):
        pass