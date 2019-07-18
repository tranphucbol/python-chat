import connect
from models.session import Session as SessionInterface

class Session(SessionInterface):

    def addSession(self, user_id, session_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('INSERT INTO sessions (user_id, session_id) VALUES (%(user_id)s, %(session_id)s)'),
            {
                'user_id': user_id,
                'session_id': session_id
            }
        )
        cnx.commit()
        cnx.close()

    def checkUserOnline(self, user_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('SELECT user_id FROM sessions WHERE user_id = %(user_id)s'),
            {
                'user_id': user_id
            }
        )

        user_id = cursor.fetchone()
        cnx.close()

        return user_id != None

    def updateSession(self, user_id, session_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('UPDATE sessions SET session_id = %(session_id)s WHERE user_id = %(user_id)s'),
            {
                'user_id': user_id,
                'session_id': session_id
            }
        )
        cnx.commit()
        cnx.close()

    def removeSession(self, session_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('DELETE FROM sessions WHERE session_id = %(session_id)s'),
            {
                'session_id': session_id
            }
        )
        cnx.commit()
        cnx.close()

    def checkSession(self, session_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('SELECT user_id FROM sessions WHERE session_id = %(session_id)s'),
            {
                'session_id': session_id
            }
        )

        raw = cursor.fetchone()
        user_id = None
        if raw != None:
            (user_id,) = raw
        cnx.close()
        return user_id