# import models.user as User
# import models.user as User
# import models.channels as Channel
# import models.message as Message
# import models.session as Session
import random
import datetime
import json
import uuid
from models.redis.user import User
from models.redis.channel import Channel

if __name__ == '__main__':
    user = User()
    channel = Channel()
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
    print(channel.getAllChannelTwoUser(user.getUserIdByUsername('tranphucbol')))

    # user = User()

    # user.addUser('tranphucbol', '123456')
    # user.addUser('tranphucbol1', '123456')
    # user.addUser('tranphucbol2', '123456')
    # user.addFriend(user.getUserIdByUsername('tranphucbol'), user.getUserIdByUsername('tranphucbol1'), 1)
    # user.addFriend(user.getUserIdByUsername('tranphucbol'), user.getUserIdByUsername('tranphucbol2'), 1)
    # print(user.getFriendAllByStatus(user.getUserIdByUsername('tranphucbol'), 1))

