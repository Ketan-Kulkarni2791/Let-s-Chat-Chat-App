from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_socketio import SocketIO, join_room, leave_room

# from db import get_user

app = Flask(__name__)
socketio = SocketIO(app)
login_manager = LoginManager()
# To connect LoginManager with my Flask application.
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')

        # This will get the user for us from database.
        # user = get_user(username)
        message = ''
        if username and username.check_password(password_input):
            # This function will log in the user.
            login_user(username)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login !'
    return render_template('login.html', message=message)


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('send_message')
def handle_send_message_event(data):
    print("{} has sent message to the room {}: {}".format(data['username'],
                                                          data['room'],
                                                          data['message']))
    socketio.emit('receive_message', data, room=data['room'])  # Message will be emitted in provided room only.


@socketio.on('join_room')
def handle_join_room_event(data):
    print("{} has joined the room {}.".format(data['username'], data['room']))
    # This will emit the message for that particular room
    join_room(data['room'])
    # This will announce to other clients in that room that someone has joined.
    socketio.emit('join_room_announcement', data)


@socketio.on('leave_room')
def handle_leave_room_event(data):
    print("{} has left the room {}".format(data['username'], data['room']))
    # This will emit the message for that particular room
    leave_room(data['room'])
    # This will announce to other clients in that room that someone has joined.
    socketio.emit('leave_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    # return get_user(username)
    return username


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    socketio.run(debug=True)
