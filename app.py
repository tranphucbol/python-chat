from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    session,
    jsonify
)

import os
import datetime
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import models.user as User
import models.channels as Channel
import models.message as Message


app = Flask(__name__)
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('connect')
def connectRoom():
    if 'user' in session:
        join_room(str(session['user']['user_id']))


@socketio.on('join')
def join(message):
    join_room(message['room'])
    # emit('my_response', {
    #     'data': 'In rooms: ' + ', '.join(rooms())
    # })


@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    # emit('my_response', {
    #     'data': 'In rooms: ' + ', '.join(rooms())
    # })


@socketio.on('close_room')
def close(message):
    # emit('my_response', {
    #     'data': 'Room ' + message['room'] + ' is closing',
    # }, room=message['room'])
    close_room(message['room'])


@socketio.on('seen_event')
def send_event_seen(event):
    print('PENG')
    emit('my_response', {
        'type': 'seen',
        'room': event['room'],
        'id': event['id']
    }, room=event['room'])


@socketio.on('my_room_event')
def send_room_message(message):

    Message.addMessage(message['room'], session['user']
                       ['user_id'], message['data'])

    emit('my_response', {
        'type': 'message',
        'data': {
            'content': message['data'],
            'time': datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        },
        'room': message['room'],
        'id': message['id']
    }, room=message['room'])


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


@app.route("/messages/<room>")
def getMessages(room):
    if 'user' in session:
        messages = Message.getAllMessage(room, session['user']['user_id'])
        return jsonify(messages)
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if User.checkUser(request.form['username'], request.form['password']):
            session['user'] = {
                'username': request.form['username'],
                'user_id': User.getUserIdByUsername(request.form['username'])
            }
            return redirect('/')

    if 'user' in session:
        return redirect('/')

    return render_template('login.html')


@app.route("/channels", methods=['GET', 'POST'])
def getChannels():
    if request.method == 'GET':
        if 'user' in session:
            channels = Channel.getAllChannel(session['user']['user_id'])
            return jsonify(channels)
        else:
            return jsonify({
                'error': 'you must login'
            })


@app.route("/friends")
def getFriends():
    if 'user' in session:
        friends = User.getFriendAllByStatus(session['user']['user_id'], 1)
        return jsonify(friends)
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route("/friend-requests", methods=['GET', 'POST'])
def getFriendRequest():
    if 'user' in session:
        user_id = session['user']['user_id']
        if request.method == 'GET':
            friendRequests = User.getFriendAllByStatus(user_id, 0)
            return jsonify(friendRequests)
        else:
            friend_id = request.form['friend_id']
            accept = int(request.form['accept'])
            if accept == 2:
                User.removeFriend(friend_id, user_id)
                return jsonify({
                    'success': 'Reject successfully'
                })
            elif accept == 1:
                User.updateStatusFriend(friend_id, user_id, accept)
                User.addFriend(user_id, friend_id, 1)
                channel_id = Channel.createChannel()
                Channel.addUserToChannel(channel_id, user_id)
                Channel.addUserToChannel(channel_id, friend_id)
                data = User.getInfoUser(user_id)

                emit('my_response', {
                    'type': 'create-room',
                    'data': {
                        'channel_id': 'room-{}'.format(channel_id),
                        'friend': session['user']['username']
                    }
                }, namespace='/', room=str(user_id))
                emit('my_response', {
                    'type': 'create-room',
                    'data': {
                        'channel_id': 'room-{}'.format(channel_id),
                        'friend': data['username']
                    }
                }, namespace='/', room=str(friend_id))

                return jsonify({
                    'friend_id': data['user_id'],
                    'username': data['username']
                })
            else:
                return jsonify({
                    'error': 'Wrong value'
                })

    else:
        return jsonify({
            'error': 'you must login'
        })

@app.route("/add-friend/<username>")
def addFriend(username):
    if 'user' in session:
        friend_id = User.getUserIdByUsername(username)
        if friend_id == None:
            return jsonify({
                'error': "username doesn't exist"
            })
        else:
            User.addFriend(session['user']['user_id'], friend_id, 0)
            emit('my_response', {
                'type': 'friend-request',
                'friend_id': session['user']['user_id'],
                'username': session['user']['username'] 
            }, namespace='/', room=str(friend_id))
            return jsonify({
                'success': "send request successfully"
            })
    else:
        return jsonify({
            'error': 'you must login'
        })

@app.route("/no-seen/<room>")
def getSeen(room):
    if 'user' in session:
        channel_id = int(room[5:len(room)])
        return jsonify({
            'count': Message.getCountNotSeen(room, session['user']['user_id']),
            'time': Message.getLastTimeMessage(channel_id)
        })
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route("/seen-user/<room>")
def getUserSeen(room):
    if 'user' in session:
        status = len(Message.getAllUserNotSeen(room)) == 0
        return jsonify({
            'status': status
        })
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route("/seen/<room>")
def updateSeen(room):
        if 'user' in session:
            Message.updateSeen(room, session['user']['user_id'])
            return jsonify({
                'sucess': 'done'
            })
        else:
            return jsonify({
                'error': 'you must login'
            })


@app.route("/")
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', user=session['user']['username'])


if (__name__ == "__main__"):
    app.secret_key = os.urandom(24)
    socketio.run(app, debug=True)
