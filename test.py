
import random
import datetime
import json
import uuid
# from models.mysql.user import User
# from models.mysql.message import Message
# from dateutil.parser import parse
from models.redis.user import User
from models.redis.channel import Channel
from models.redis.message import Message

if __name__ == '__main__':
    user = User()
    channel = Channel()
    message = Message()
    user.addUser('tranphucbol', '123456')
    for x in range(0, 15):
        user.addUser('tranphucbol{}'.format(x), '123456')
    for x in range(0, 10):
        user_id = user.getUserIdByUsername('tranphucbol')
        friend_id = user.getUserIdByUsername('tranphucbol{}'.format(x))
        user.addFriend(user_id, friend_id, 1)
        user.addFriend(friend_id, user_id, 1)
        id = channel.createChannel()
        channel.addUserToChannel(id, user_id)
        channel.addUserToChannel(id, friend_id)
        # print(message.getCountNotSeen(id, user_id))
