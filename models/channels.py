import models.user as User
import connect

def createChannel():
    cnx = connect.createConnect()
    cursor = cnx.cursor()
    cursor.execute(
        ('INSERT INTO channels () values ()')
    )
    id = cursor.lastrowid
    cnx.commit()
    cnx.close()
    return id

def addUserToChannel(channel_id, username):
    cnx = connect.createConnect()
    user_id = User.getUserIdByUsername(username)
    cursor = cnx.cursor()
    cursor.execute(
        ('INSERT INTO users_channels (user_id, channel_id) values (%(user_id)s, %(channel_id)s)'),
        {
            'user_id': user_id,
            'channel_id': channel_id
        }
    )
    cnx.commit()
    cnx.close()

def getAllChannel(username):
    cnx = connect.createConnect()
    user_id = User.getUserIdByUsername(username)
    cursor = cnx.cursor()
    cursor.execute(
        ('SELECT uc.channel_id as channel_id, u.username as friend  FROM users_channels as uc, users_channels as fc, users as u WHERE uc.user_id = %(user_id)s AND uc.channel_id = fc.channel_id AND fc.user_id <> %(user_id)s AND u.user_id = fc.user_id'),
        {
            'user_id': user_id
        }
    )

    channels = []
    for (channel_id, friend,) in cursor:
        channels.append({
            'channel_id': 'room-{}'.format(channel_id),
            'friend': friend
    })
    cnx.close()
    return channels
    