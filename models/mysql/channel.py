import connect
import datetime
import uuid
from models.mysql.user import User
from models.mysql.message import Message
from models.mysql.session import Session
from models.channel import Channel as ChannelInterface

class Channel(ChannelInterface):

    def createChannel(self):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        id = str(uuid.uuid1())
        cursor.execute(
            ('INSERT INTO channels (channel_id) values (%(channel_id)s)'),
            {
                'channel_id': id
            }
        )
        cnx.commit()
        cnx.close()
        return id

    def addUserToChannel(self, channel_id, user_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('INSERT INTO users_channels (user_id, channel_id, seen) values (%(user_id)s, %(channel_id)s, now())'),
            {
                'user_id': user_id,
                'channel_id': channel_id,
            }
        )
        cnx.commit()
        cnx.close()

    def getAllChannelTwoUser(self, user_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            'SELECT uc.channel_id '
            'FROM users_channels uc, users_channels fc '
            'WHERE uc.user_id = %(user_id)s '
            'AND uc.channel_id = fc.channel_id '
            'AND fc.user_id <> %(user_id)s '
            'GROUP BY uc.channel_id '
            'HAVING COUNT(uc.user_id)',
            {
                'user_id': user_id
            }
        )
        channels = []
        for (channel_id,) in cursor:
            channels.append(channel_id)
        cnx.close()
        return channels

    def getAllChannel(self, user_id):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('SELECT uc.channel_id, COUNT(uc.user_id) as count '
            'FROM users_channels uc, users_channels fc '
            'WHERE uc.user_id = %(user_id)s '
            'AND uc.channel_id = fc.channel_id '
            'AND fc.user_id <> %(user_id)s '
            'GROUP BY uc.channel_id'),
            {
                'user_id': user_id
            }
        )

        channels = []
        for (channel_id, count,) in cursor:
            friend = {}
            if count == 1:
                friend['name'] = self.getChannelName(channel_id, user_id)
                friend['id'] = User().getUserIdByUsername(friend['name'])
                friend['online'] = Session().checkUserOnline(friend['id'])
            else:
                print('peng')
                friend['name'] = getChannelName(channel_id)
            channels.append({
                'channel_id': channel_id,
                'friend': friend,
                'last_reaction': Message().getLastTimeMessage(channel_id)
        })
        cnx.close()
        channels.sort(key=self.sortChannels, reverse=True)
        return channels

    def sortChannels(self, channel):
        return channel['last_reaction']
        
    def getChannelName(self, channel_id, user_id=None):
        cnx = connect.createConnect()
        cursor = cnx.cursor()
        cursor.execute(
            ('SELECT name FROM channels WHERE channel_id = %(channel_id)s'),
            {
                'channel_id': channel_id
            }
        )
        (name,) = cursor.fetchone()
        if name == None:
            cursor.execute(
            ('SELECT u.username, u.user_id as uid FROM users u, users_channels uc WHERE uc.channel_id = %(channel_id)s AND u.user_id = uc.user_id'),
                {
                    'channel_id': channel_id
                }
            )
            name = ''
            for (username, uid,) in cursor:
                if user_id != uid:
                    name = str(name) + str(username) + ', '
            name = name[0:len(name)-2]
        cnx.close()
        return name