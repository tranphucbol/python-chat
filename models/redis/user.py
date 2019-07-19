import connectRedis as connect
import uuid
import bcrypt
import datetime
from models.user import User as UserInterface
from models.redis.session import Session


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
        pw = r.hget('users:{}'.format(username), 'password')
        if pw != None and bcrypt.checkpw(password.encode('utf-8'), pw):
            return True
        return False

    def getUserIdByUsername(self, username):
        r = connect.createConnect()
        data = r.hget('users:{}'.format(username), 'user_id').decode('utf-8')
        return data

    def checkUserExist(self, username):
        r = connect.createConnect()
        return True if r.exists('users:{}'.format(username)) == 1 else False

    def addFriend(self, user_id, friend_id, status):
        r = connect.createConnect()
        r.hmset('friends:{}:{}'.format(user_id, friend_id), {
            'user_id': user_id,
            'friend_id': friend_id,
            'status': status
        })

    def getFriendAllByStatus(self, user_id, status):
        r = connect.createConnect()
        keys = r.keys('friends:*:{}'.format(user_id))
        friends = []
        for key in keys:
            s = int(r.hget(key, 'status').decode('utf-8'))
            friend_id = r.hget(key, 'user_id').decode('utf-8')
            username = r.hget('user_infos:{}'.format(friend_id), 'username')
            if s == status:
                friends.append({
                    'friend_id': friend_id,
                    'username': username,
                    'online': Session().checkUserOnline(friend_id)
                })

        return friends

    def updateStatusFriend(self, user_id, friend_id, status):
        r = connect.createConnect()
        r.hmset('friends:{}:{}'.format(user_id, friend_id), {
            'friend_id': friend_id,
            'status': status
        })

    def removeFriend(self, user_id, friend_id):
        pass

    def getInfoUser(self, user_id):
        r = connect.createConnect()
        return {
            'username': r.hget('user_infos:{}'.format(user_id), 'username').decode('utf-8'),
            'user_id': user_id
        }
