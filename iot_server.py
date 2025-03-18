from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('led_state')
def handle_led_state(data):
    print(f"LED state changed: {'ON' if data['state'] else 'OFF'}")
    socketio.emit('led_state', data)  # Update frontend

if __name__ == '__main__':
    socketio.run(app, debug=True)
