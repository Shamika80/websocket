from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY']  = 'your_secret_key'
socketio = SocketIO(app) 

message_storage = {}

@app.route('/')
def index():
    return render_template('index.html')

def handle_message(data):
    author = data['author']
    message = data['message']

    if author in message_storage:
        message_storage[author].append(message)
    else:
        message_storage[author] = [message]

    messages_for_author = message_storage.get(author, [])
    emit('message_response', {'author': author, 'messages': messages_for_author}, room=request.sid)

socketio.on('message')(handle_message)  

if __name__ == '__main__':
    socketio.run(app)