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
        'createdAt': datetime.datetime.now(),
        'updatedAt' : datetime.datetime.now()
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

def addFriend(username, usernameOfFriend):
    cnx = connect.createConnect()
    print('hello')
    data = {
        'user_id': getUserIdByUsername(username),
        'friend_id': getUserIdByUsername(usernameOfFriend),
        'status': 1
    }

    print(data)

    cursor = cnx.cursor()
    cursor.execute(
        ("INSERT INTO friends (user_id, friend_id, status) VALUES (%(user_id)s, %(friend_id)s, %(status)s)"),
        data
    )
    cnx.commit()
    cnx.close()

def getAllFriend(username):
    cnx = connect.createConnect()
    cQuery = cnx.cursor()
    cQuery.execute(
        ("SELECT ufriends.username FROM users, friends, users as ufriends WHERE users.username = %(username)s AND users.user_id = friends.user_id AND friends.friend_id = ufriends.user_id"),
        {'username': username}
    )

    friends = []

    for (username,) in cQuery:
        friends.append(username)
    cnx.close()
    return friends