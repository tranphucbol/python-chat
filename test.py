# import models.user as User
import models.user as User
import models.channels as Channel
import random

if __name__ == '__main__':
    # User.addUser('tranphucbol', 'tranphucbol@gmail.com', '123456')
    # for x in range(0, 10):
    #     User.addUser('tranphucbol{}'.format(x), 'tranphucbol{}@gmail.com', '123456')
    # for x in range(0, 10):
    #     User.addFriend('tranphucbol', 'tranphucbol{}'.format(x))
    #     User.addFriend('tranphucbol{}'.format(x), 'tranphucbol')
    #     id = Channel.createChannel()
    #     Channel.addUserToChannel(id, 'tranphucbol')
    #     Channel.addUserToChannel(id, 'tranphucbol{}'.format(x))
    channels = Channel.getAllChannel('tranphucbol')
    # for channel in channels:
    #     print(channel['friend'])
    print(channels[0])
