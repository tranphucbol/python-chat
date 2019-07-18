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

    user = User()

    user.addUser('tranphucbol', '123456')
    user.addUser('tranphucbol1', '123456')
    user.addUser('tranphucbol2', '123456')
    user.addFriend(user.getUserIdByUsername('tranphucbol'), user.getUserIdByUsername('tranphucbol1'), 1)
    user.addFriend(user.getUserIdByUsername('tranphucbol'), user.getUserIdByUsername('tranphucbol2'), 1)
    print(user.getFriendAllByStatus(user.getUserIdByUsername('tranphucbol'), 1))

