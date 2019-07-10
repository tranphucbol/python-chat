# import models.user as User
import models.user as User
import models.channels as Channel
import models.message as Message
import random

if __name__ == '__main__':
    # User.addUser('tranphucbol', 'tranphucbol@gmail.com', '123456')
    for x in range(11, 13):
        User.addUser('tranphucbol{}'.format(x), 'tranphucbol{}@gmail.com'.format(x), '123456')
    for x in range(11, 13):
        user_id = User.getUserIdByUsername('tranphucbol')
        friend_id = User.getUserIdByUsername('tranphucbol{}'.format(x))
        User.addFriend(user_id, friend_id)
        User.addFriend(friend_id, user_id)
        id = Channel.createChannel()
        Channel.addUserToChannel(id, user_id)
        Channel.addUserToChannel(id, friend_id)
    # channels = Channel.getAllChannel('tranphucbol')
    # for channel in channels:
    #     print(channel['friend'])

