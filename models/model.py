from models.redis.user import User as UserRedis
from models.redis.session import Session as SessionRedis
from models.redis.channel import Channel as ChannelRedis
from models.redis.message import Message as MessageRedis

from models.mysql.user import User as UserMySQL
from models.mysql.session import Session as SessionMySQL
from models.mysql.channel import Channel as ChannelMySQL
from models.mysql.message import Message as MessageMySQL

class Model:
    def __init__(self, db):
        if(db == 'redis'):
            self.User = UserRedis()
            self.Session = SessionRedis()
            self.Channel = ChannelRedis()
            self.Message = MessageRedis()
        else:
            self.User = UserMySQL()
            self.Session = SessionMySQL()
            self.Channel = ChannelMySQL()
            self.Message = MessageMySQL()