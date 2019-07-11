# import models.user as User
import models.user as User
import models.channels as Channel
import models.message as Message
import random

if __name__ == '__main__':
    # User.addUser('tranphucbol', 'tranphucbol@gmail.com', '123456')
    # for x in range(13, 15):
    #     User.addUser('tranphucbol{}'.format(x), 'tranphucbol{}@gmail.com'.format(x), '123456')
    #     User.addFriend(User.getUserIdByUsername('tranphucbol{}'.format(x)), User.getUserIdByUsername('tranphucbol'), 0)
    # for x in range(0, 10):
    #     user_id = User.getUserIdByUsername('tranphucbol')
    #     friend_id = User.getUserIdByUsername('tranphucbol{}'.format(x))
    #     User.addFriend(user_id, friend_id)
    #     User.addFriend(friend_id, user_id)
    #     id = Channel.createChannel()
    #     Channel.addUserToChannel(id, user_id)
    #     Channel.addUserToChannel(id, friend_id)
    # channels = Channel.getAllChannel('tranphucbol')
    # for channel in channels:
    #     print(channel['friend'])

    User.updateStatusFriend(1, 15, 0)
    print(User.getFriendAllByStatus(1, 0))