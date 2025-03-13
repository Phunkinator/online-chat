from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

nicknames = set()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/set_nickname', methods=['POST'])
def set_nickname():
    nickname = request.form.get('nickname')
    if nickname in nicknames:
        return redirect(url_for('index'))
    else:
        nicknames.add(nickname)
        return render_template('chat.html', nickname=nickname)

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room: {}".format(data['nickname'], data['message']))
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)