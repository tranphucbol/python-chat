import connectRedis as connect
from models.session import Session as SessionInterface

class Session(SessionInterface):

    def addSession(self, user_id, session_id):
        r = connect.createConnect()
        r.hmset(
            'sessions:{}:{}'.format(user_id, session_id),
            {
                'user_id': user_id,
                'session_id': session_id
            }
        )

    def checkUserOnline(self, user_id):
        r = connect.createConnect()
        keys = r.keys('sessions:{}:*'.format(user_id))
        c = 0
        for key in keys:
            c = r.exists(key)
        return True if c == 1 else False

    def updateSession(self, user_id, session_id):
        self.removeSession(session_id)
        self.addSession(user_id, session_id)
    
    def removeSession(self, session_id):
        r = connect.createConnect()
        r.delete('sessions:*:{}'.format(session_id))

    def checkSession(self, session_id):
        r = connect.createConnect()
        keys = r.keys('sessions:*:{}'.format(session_id))
        user_id = None
        for key in keys:
            user_id = r.hget(key, 'user_id')
        return user_id