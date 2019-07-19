import connectRedis as connect
import datetime
import uuid
from models.channel import Channel as ChannelInterface

class Channel(ChannelInterface):

    def createChannel(self):
        r = connect.createConnect()
        id = str(uuid.uuid1())
        r.hmset('channels:{}'.format(id), {'channel_id': id, 'name': ''})
        return id

    def addUserToChannel(self, channel_id, user_id):
        r = connect.createConnect()
        r.hmset(
            'users_channels:{}:{}'.format(channel_id, user_id),
            {
                'channel_id': channel_id,
                'user_id': user_id,
                'seen': datetime.datetime.now().__repr__()
            }
        )

    def getAllChannelTwoUser(self, user_id):
        r = connect.createConnect()
        keys = r.keys('users_channels:*:{}'.format(user_id))
        channels = []
        for key in keys:
            channel_id = r.hmget(key, 'channel_id')
            count = len(r.keys('user_channels:{}:*'.format(channel_id)))
            if count == 2:
                channels.append(channel_id)
        return channels

    def getAllChannel(self, user_id):
        pass
    
    def getChannelName(self, channel_id, user_id=None):
        pass