import connectRedis as connect
import uuid
import bcrypt

def addUser(username, password):
    r = connect.createConnect()
    user_id = str(uuid.uuid1())
    data = {
        'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        'user_id': user_id
    }
    r.hmset('users:{}'.format(username), data)

def getUserIdByUsername(username):
    r = connect.createConnect()
    data = r.hget('users:{}'.format(username), 'user_id').decode('utf-8')
    return data