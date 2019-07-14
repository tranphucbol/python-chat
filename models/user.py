import datetime
import bcrypt
import connect
import array as arr

def addUser(username, email, password):
    data_user = {
        'username': username,
        'email': email,
        'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        'status': 1,
        'createdAt': datetime.datetime.now().astimezone(),
        'updatedAt' : datetime.datetime.now().astimezone()
    }

    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursor.execute(
        ("INSERT INTO users (username, email, password, status, created_at, updated_at) VALUES (%(username)s, %(email)s, %(password)s, %(status)s, %(createdAt)s, %(updatedAt)s)"),
        data_user
    )
    cnx.commit()
    cursor.close()
    cnx.close()

def checkUser(username, password):
    print('ping')
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

def getUserIdByUsername(username):
    cnx = connect.createConnect()
    cQuery = cnx.cursor()
    cQuery.execute(
        ("SELECT user_id as id FROM users WHERE username = %(username)s"),
        {'username': username}
    )
    (id,) = cQuery.fetchone()
    return id

def addFriend(user_id, friend_id, status):
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

def getFriendAllByStatus(user_id, status):
    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursor.execute(
        ('SELECT u.user_id as friend_id, u.username as username FROM users u, friends f WHERE f.friend_id = %(user_id)s AND f.status = %(status)s AND f.user_id = u.user_id'),
        {
            'user_id': user_id,
            'status': status
        }
    )
    friendRequests = []
    for (friend_id, username,) in cursor:
        friendRequests.append({
            'friend_id': friend_id,
            'username': username
        })
    cnx.close()
    return friendRequests

def updateStatusFriend(user_id, friend_id, status):
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

def removeFriend(user_id, friend_id):
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

def getInfoUser(user_id):
    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursor.execute(
        ("SELECT user_id, username FROM users WHERE user_id = %(user_id)s"),
        {
            'user_id': user_id
        }
    )
    (user_id, username,) = cursor.fetchone()
    cnx.close()
    return {
        'user_id': user_id,
        'username': username
    }

# def getAllFriend(user_id):
#     cnx = connect.createConnect()
#     cQuery = cnx.cursor()
#     cQuery.execute(
#         ("SELECT ufriends.username FROM users, friends, users as ufriends WHERE users.username = %(username)s AND users.user_id = friends.user_id AND friends.friend_id = ufriends.user_id"),
#         {'username': username}
#     )

#     friends = []

#     for (username,) in cQuery:
#         friends.append(username)
#     cnx.close()
#     return friends