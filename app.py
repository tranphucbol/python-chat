from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    session,
)

import os
import datetime
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room


app = Flask(__name__)
socketio = SocketIO(app)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.send(username + ' has left the room.', room=room)

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        return redirect('/')
    return render_template('login.html')

@app.route("/")
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html', user=session['user'])

if (__name__ == "__main__"):
    app.secret_key = os.urandom(24)
    socketio.run(app, debug=True)