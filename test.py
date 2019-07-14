# import models.user as User
import models.user as User
import models.channels as Channel
import models.message as Message
import random
import datetime
import json

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
if __name__ == '__main__':
    # User.addUser('tranphucbol', 'tranphucbol@gmail.com', '123456')
    # for x in range(0, 10):
    #     User.addUser('tranphucbol{}'.format(x), 'tranphucbol{}@gmail.com'.format(x), '123456')
    # for x in range(0, 10):
    #     user_id = User.getUserIdByUsername('tranphucbol')
    #     friend_id = User.getUserIdByUsername('tranphucbol{}'.format(x))
    #     User.addFriend(user_id, friend_id, 1)
    #     User.addFriend(friend_id, user_id, 1)
    #     id = Channel.createChannel()
    #     Channel.addUserToChannel(id, user_id)
    #     Channel.addUserToChannel(id, friend_id)

    # channels = Channel.getAllChannel(User.getUserIdByUsername('tranphucbol0'))
    # for channel in channels:
    #     print(channel['friend'])
    # messages = Message.getAllMessage('room-1', 1);
    # for message in messages:
    #     print(message)
    Message.updateSeen('room-1', 1)
    print(Message.getCountNotSeen('room-1', 1))
