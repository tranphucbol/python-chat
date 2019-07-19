import connectRedis as connect
import datetime
import uuid
from models.channel import Channel as ChannelInterface
from models.redis.user import User
from models.redis.session import Session
from models.redis.message import Message

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
                'seen': str(datetime.datetime.now())
            }
        )

    def getAllChannelTwoUser(self, user_id):
        r = connect.createConnect()
        keys = r.keys('users_channels:*:{}'.format(user_id))
        channels = []
        for key in keys:
            channel_id = r.hget(key, 'channel_id').decode('utf-8')
            count = len(r.keys('users_channels:{}:*'.format(channel_id)))
            if count == 2:
                channels.append(channel_id)
        return channels

    def getAllChannel(self, user_id):
        r = connect.createConnect()
        keys = r.keys('users_channels:*:{}'.format(user_id))
        channels = []
        for key in keys:
            friend = {}
            channel_id = r.hget(key, 'channel_id').decode('utf-8')
            count = len(r.keys('users_channels:{}:*'.format(channel_id)))
            if count == 2:
                friend['name'] = self.getChannelName(channel_id, user_id)
                friend['id'] = User().getUserIdByUsername(friend['name'])
                friend['online'] = Session().checkUserOnline(friend['id'])
            else:
                friend['name'] = self.getChannelName(channel_id)
            channels.append({
                        'channel_id': channel_id,
                        'friend': friend,
                        'last_reaction': Message().getLastTimeMessage(channel_id)
                    })
        channels.sort(key=self.sortChannels, reverse=True)
        return channels

    def sortChannels(self, channel):
        return channel['last_reaction']
    
    def getChannelName(self, channel_id, user_id=None):
        r = connect.createConnect()
        channel_name = r.hget('channels:{}'.format(channel_id), 'name').decode('utf-8');
        if channel_name == '':
            keys = r.keys('users_channels:{}:*'.format(channel_id))
            for key in keys:
                uid = r.hget(key, 'user_id').decode('utf-8')
                if uid != user_id:
                    username = r.hget('user_infos:{}'.format(uid), 'username').decode('utf-8')
                    channel_name = channel_name +  username + ', '
            channel_name = channel_name[0:len(channel_name)-2]
        return channel_name