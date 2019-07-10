import datetime
import connect

def addMessage(room, author_id, message):
    channel_id = int(room[5:len(room)])
    data = {
        'channel_id': channel_id,
        'author_id': author_id,
        'content': message,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now() 
    }

    cnx = connect.createConnect()
    cursor = cnx.cursor()

    cursor.execute(
        ('INSERT INTO messages (channel_id, author_id, content, created_at, updated_at) VALUES (%(channel_id)s, %(author_id)s, %(content)s, %(created_at)s, %(updated_at)s)'),
        data
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
            'content': content,
            'updated_at': updated_at
        })

    cnx.close()

    return messages
