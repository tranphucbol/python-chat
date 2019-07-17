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
import models.session as Session


app = Flask(__name__)
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('connect')
def connectRoom():
    if 'user' in session:
        user_id = session['user']['user_id']
        join_room(user_id)
        if Session.checkUserOnline(user_id):
            Session.updateSession(user_id, request.sid)
        else:
            Session.addSession(user_id, request.sid)

        friends = User.getFriendAllByStatus(user_id, 1)
        for friend in friends:
            emit('my_response', {
                'type': 'online-status',
                'friend_id': user_id,
                'online': True
            }, namespace="/", room=friend['friend_id'])


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
    user_id = Session.checkSession(request.sid)
    if user_id != None:
        Session.removeSession(request.sid)
        friends = User.getFriendAllByStatus(user_id, 1)
        for friend in friends:
            emit('my_response', {
                'type': 'online-status',
                'friend_id': user_id,
                'online': False
            }, namespace="/", room=friend['friend_id'])


@app.route("/messages/<channel_id>")
def getMessages(channel_id):
    if 'user' in session:
        messages = Message.getAllMessage(
            channel_id, session['user']['user_id'])
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

@app.route("/register", methods=['GET', 'POST'])
def register    ():
    if request.method == 'POST':
        if User.checkUserExist(request.form['username']) == False and request.form['password'] == request.form['re-password']:
            print(request.form)
            User.addUser(request.form['username'], request.form['password'])
            session['user'] = {
                'username': request.form['username'],
                'user_id': User.getUserIdByUsername(request.form['username'])
            }
            return redirect('/')

    if 'user' in session:
        return redirect('/')

    return render_template('register.html')


@app.route("/channels", methods=['GET', 'POST'])
def getChannels():
    if 'user' in session:
        if request.method == 'GET':
            channels = Channel.getAllChannel(session['user']['user_id'])
            return jsonify(channels)
        else:
            friends = request.form.getlist('friends[]')
            channel_id = Channel.createChannel()
            Channel.addUserToChannel(channel_id, session['user']['user_id'])
            for friend in friends:
                if friend != session['user']['username'] and User.checkUserExist(friend):
                    friend_id = User.getUserIdByUsername(friend)
                    Channel.addUserToChannel(channel_id, friend_id)

            for friend in friends:
                if friend != session['user']['username'] and User.checkUserExist(friend):
                    friend_id = User.getUserIdByUsername(friend)
                    emit('my_response', {
                        'type': 'create-room',
                        'data': {
                            'channel_id': channel_id,
                            'friend': {
                                'name': Channel.getChannelName(channel_id)
                            }
                        }
                    }, namespace="/", room=friend_id)
            return jsonify({
                'channel_id': channel_id,
                'friend': {
                    'name': Channel.getChannelName(channel_id)
                }
            })

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
                data = User.getInfoUser(friend_id)

                emit('my_response', {
                    'type': 'create-room',
                    'data': {
                        'channel_id': channel_id,
                        'friend': {
                            'name': session['user']['username'],
                            'online': True
                        }
                    }
                }, namespace='/', room=str(friend_id))
                emit('my_response', {
                    'type': 'create-room',
                    'data': {
                        'channel_id': channel_id,
                        'friend': {
                            'name': data['username'],
                            'online': Session.checkUserOnline(friend_id)
                        }
                    }
                }, namespace='/', room=str(user_id))

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


@app.route("/no-seen/<channel_id>")
def getSeen(channel_id):
    if 'user' in session:
        return jsonify({
            'count': Message.getCountNotSeen(channel_id, session['user']['user_id']),
            'time': Message.getLastTimeMessage(channel_id)
        })
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route("/seen-user/<channel_id>")
def getUserSeen(channel_id):
    if 'user' in session:
        status = len(Message.getAllUserNotSeen(channel_id)) == 0
        return jsonify({
            'status': status
        })
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route("/seen/<channel_id>")
def updateSeen(channel_id):
        if 'user' in session:
            Message.updateSeen(channel_id, session['user']['user_id'])
            return jsonify({
                'success': 'done'
            })
        else:
            return jsonify({
                'error': 'you must login'
            })


@app.route("/check-user/<username>")
def checkUser(username):
    print(username)
    if 'user' in session:
        return jsonify({
            'exist': User.checkUserExist(username)
        })
    else:
        return jsonify({
            'error': 'you must login'
        })


@app.route('/logout')
def sign_out():
    session.pop('user')
    return redirect("/login")


@app.route("/")
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', user=session['user']['username'])


if (__name__ == "__main__"):
    app.secret_key = os.urandom(24)
    socketio.run(app, debug=True)
