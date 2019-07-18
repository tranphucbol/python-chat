# import models.user as User
# import models.user as User
# import models.channels as Channel
# import models.message as Message
# import models.session as Session
import random
import datetime
import json
import uuid
from models.mysql.user import User

if __name__ == '__main__':
    # User.addUser('tranphucbol', '123456')
    # for x in range(0, 15):
    #     User.addUser('tranphucbol{}'.format(x), '123456')
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
    #     print(channel)
    # messages = Message.getAllMessage('room-1', 1);
    # for message in messages:
    #     print(message)
    # print(User.getUserIdByUsername('tranphucbol'));
    # Session.addSession('e0d0d99c-a79f-11e9-9352-7446a0975f65', '6d4f6a7f451f48bf91f5c3881e182c3f')

    # UserRedis.addUser('tranphucbol', '1233456')
    # user = User()
    print(User().getUserIdByUsername('tranphucbol'))
