import connectRedis as connect
import uuid
import datetime
from models.message import Message as MessageInterface

class Message(MessageInterface):
    
    def addMessage(self, channel_id, author_id, message):
        id = str(uuid.uuid1())
        data = {
            'message_id': id,
            'channel_id': channel_id,
            'author_id': author_id,
            'content': message,
            'created_at': str(datetime.datetime.now()),
            'updated_at': str(datetime.datetime.now())
        }

        r = connect.createConnect()
        r.hmset('messages:{}:{}:{}'.format(channel_id, author_id, id), data)

    def getAllMessage(self, channel_id, user_id):
        r = connect.createConnect()
        messages = []
        keys = r.keys('messages:{}:*:*'.format(channel_id))
        for key in keys:
            author_id = r.hget(key, 'author_id').decode('utf-8')
            content = r.hget(key, 'content').decode('utf-8')
            time_str = r.hget(key, 'updated_at').decode('utf-8')
            if author_id == user_id:
                author_id = -1
            messages.append({
                'author_id': author_id,
                'data': {
                    'content': content,
                    'time': datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
                }
            })
        return messages
    
    def getCountNotSeen(self, channel_id, user_id):
        r = connect.createConnect()
        seen = r.hget('users_channels:{}:{}'.format(channel_id, user_id), 'seen').decode('utf-8')
        keys = r.keys('users_channels:{}:*'.format(channel_id))
        count = 0
        for key in keys:
            updated_at = r.hget(key, 'updated_at')
            if updated_at != None and updated_at.decode('utf-8') > seen:
                count = count + 1
        return count
    
    def updateSeen(self, channel_id, user_id):
        r = connect.createConnect()
        r.hset('users_channels:{}:{}'.format(channel_id, user_id), 'seen', str(datetime.datetime.now()))

    def getLastTimeMessage(self, channel_id):
        r = connect.createConnect()
        updated_at = None
        keys = r.keys('messages:{}:*:*'.format(channel_id))
        for key in keys:
            time_str = r.hget(key, 'updated_at').decode('utf-8')
            date = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
            if updated_at == None or updated_at < date:
                updated_at = date

        if updated_at == None:
            updated_at = datetime.datetime(2000, 1, 1)

        return updated_at

    def getAllUserNotSeen(self, channel_id):
        r = connect.createConnect()
        lastTime = self.getLastTimeMessage(channel_id)
        keys = r.keys('users_channels:{}:*'.format(channel_id))
        uids = []
        for key in keys:
            time_str = r.hget(key, 'seen').decode('utf-8')
            seen = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
            if(lastTime > seen):
                uids.append(r.hget(key, 'user_id').decode('utf-8'))
        return uids