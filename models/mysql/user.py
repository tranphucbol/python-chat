import datetime
import bcrypt
import connect
import uuid
from models.mysql.session import Session
from models.user import User as UserInterface

class User(UserInterface):

    def addUser(self, username, password):
        data_user = {
            'user_id': str(uuid.uuid1()),
            'username': username,
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            'status': 1,
            'createdAt': datetime.datetime.now().astimezone(),
            'updatedAt' : datetime.datetime.now().astimezone()
        }

        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ("INSERT INTO users (user_id, username, password, status, created_at, updated_at) VALUES (%(user_id)s, %(username)s, %(password)s, %(status)s, %(createdAt)s, %(updatedAt)s)"),
            data_user
        )
        cnx.commit()
        cursor.close()
        cnx.close()

    def checkUser(self, username, password):
        cnx = connect.createConnect()
        cQuery = cnx.cursor()
        cQuery.execute(
            ("SELECT username as uname, password as pw FROM users WHERE username = %(username)s"),
            {'username': username}
        )
        for(uname, pw) in cQuery:
            if(bcrypt.checkpw(password.encode('utf-8'), pw.encode('utf-8'))):
                cnx.close()
                return True
        cnx.close()
        return False

    def checkUserExist(self, username):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ("SELECT user_id FROM users WHERE username = %(username)s"),
            {'username': username}
        )
        user = cursor.fetchone()
        cnx.close()
        return user != None

    def getUserIdByUsername(self, username):
        cnx = connect.createConnect()
        cQuery = cnx.cursor()
        cQuery.execute(
            ("SELECT user_id as id FROM users WHERE username = %(username)s"),
            {'username': username}
        )
        id_fetch = cQuery.fetchone()
        id = None
        if(id_fetch != None):
            (id,) = id_fetch
        cnx.close()
        return id

    def addFriend(self, user_id, friend_id, status):
        cnx = connect.createConnect()
        data = {
            'user_id': user_id,
            'friend_id': friend_id,
            'status': status
        }

        cursor = cnx.cursor()
        cursor.execute(
            ("INSERT INTO friends (user_id, friend_id, status) VALUES (%(user_id)s, %(friend_id)s, %(status)s)"),
            data
        )
        cnx.commit()
        cnx.close()

    def getFriendAllByStatus(self, user_id, status):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('SELECT u.user_id as friend_id, u.username as username FROM users u, friends f WHERE f.friend_id = %(user_id)s AND f.status = %(status)s AND f.user_id = u.user_id'),
            {
                'user_id': user_id,
                'status': status
            }
        )
        friends = []
        for (friend_id, username,) in cursor:
            friends.append({
                'friend_id': friend_id,
                'username': username,
                'online': Session().checkUserOnline(friend_id)
            })
        cnx.close()
        return friends

    def updateStatusFriend(self, user_id, friend_id, status):
        cnx = connect.createConnect()
        data = {
            'user_id': user_id,
            'friend_id': friend_id,
            'status': status
        }

        cursor = cnx.cursor()
        cursor.execute(
            ("UPDATE friends SET status = %(status)s WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s"),
            data
        )
        cnx.commit()
        cnx.close()

    def removeFriend(self, user_id, friend_id):
        cnx = connect.createConnect()
        data = {
            'user_id': user_id,
            'friend_id': friend_id
        }

        cursor = cnx.cursor()
        cursor.execute(
            ("DELETE FROM friends WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s"),
            data
        )
        cnx.commit()
        cnx.close()

    def getInfoUser(self, user_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ("SELECT user_id, username FROM users WHERE user_id = %(user_id)s"),
            {
                'user_id': user_id
            }
        )
        (user_id, username) = cursor.fetchone()
        cnx.close()
        return {
            'user_id': user_id,
            'username': username
        }