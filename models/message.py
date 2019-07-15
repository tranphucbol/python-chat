import datetime
import connect


def addMessage(room, author_id, message):
    channel_id = int(room[5:len(room)])
    data = {
        'channel_id': channel_id,
        'author_id': author_id,
        'content': message
    }

    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursorSeen = cnx.cursor()

    cursor.execute(
        ('INSERT INTO messages (channel_id, author_id, content, created_at, updated_at) VALUES (%(channel_id)s, %(author_id)s, %(content)s, now(), now())'),
        data
    )
    cursorSeen.execute(
        ('UPDATE users_channels SET seen = now() WHERE user_id = %(user_id)s AND channel_id = %(channel_id)s'),
        {
            'user_id': author_id,
            'channel_id': channel_id
        }
    )
    cnx.commit()

    cnx.close()


def getAllMessage(room, user_id):
    channel_id = int(room[5:len(room)])
    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursor.execute(
        ('SELECT author_id, updated_at, content FROM messages WHERE channel_id = %(channel_id)s'),
        {
            'channel_id': channel_id
        }
    )

    messages = []

    for (author_id, updated_at, content, ) in cursor:
        if author_id == user_id:
            author_id = -1
        messages.append({
            'author_id': author_id,
            'data': {
                'content': content,
                'time': updated_at,
            }
        })

    cnx.close()

    return messages


def getCountNotSeen(room, user_id):
    channel_id = int(room[5:len(room)])
    cnx = connect.createConnect()
    cursor = cnx.cursor()

    cursor.execute(
        ('SELECT COUNT(m.message_id) as count '
         'FROM users_channels uc, messages m '
         'WHERE uc.user_id = %(user_id)s '
         'AND uc.channel_id = %(channel_id)s '
         'AND m.channel_id = %(channel_id)s '
         'AND m.updated_at > uc.seen'),
        {
            'user_id': user_id,
            'channel_id': channel_id
        }
    )
    (count,) = cursor.fetchone()
    cnx.close()
    return count


def updateSeen(room, user_id):
    channel_id = int(room[5:len(room)])
    cnx = connect.createConnect()
    cursor = cnx.cursor()

    cursor.execute(
        ('UPDATE users_channels SET seen = now() WHERE user_id = %(user_id)s AND channel_id = %(channel_id)s'),
        {
            'user_id': user_id,
            'channel_id': channel_id
        }
    )

    cnx.commit()
    cnx.close()


def getLastTimeMessage(channel_id):
    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursor.execute(
        ('SELECT MAX(updated_at) as date FROM messages WHERE channel_id = %(channel_id)s'),
        {
            'channel_id': channel_id
        }
    )
    (date,) = cursor.fetchone()
    if date == None:
        date = datetime.datetime(2000, 1, 1)
    cnx.close()
    return date

def getAllUserNotSeen(room):
    channel_id = int(room[5:len(room)])
    cnx = connect.createConnect();
    cursor = cnx.cursor()
    cursor.execute(
        ('SELECT uc.user_id '
        'FROM users_channels uc, messages m '
        'WHERE uc.channel_id = %(channel_id)s '
        'AND uc.channel_id = m.channel_id '
        'AND m.updated_at > uc.seen '
        'GROUP BY uc.user_id'),
        {
            'channel_id': channel_id
        }
    )
    users = []
    for (user_id,) in cursor:
        users.append(user_id)
    cnx.close()
    return users
