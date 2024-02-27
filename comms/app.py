from flask import Flask
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Placeholder for storing messages
messages = {
    "northbound": {
        "aspirational_layer": [],
        "global_strategy": [],
        "agent_model": [],
        "executive_function": [],
        "cognitive_control": [],
        "task_prosecution": []
    },
    "southbound": {
        "aspirational_layer": [],
        "global_strategy": [],
        "agent_model": [],
        "executive_function": [],
        "cognitive_control": [],
        "task_prosecution": []
    }
}

# SocketIO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    app.logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    app.logger.info('Client disconnected')

@socketio.on('post_message')
def handle_post_message(data):
    try:
        direction = data['direction']
        layer = data['layer']
        message = data['message']
        if direction in messages and layer in messages[direction]:
            messages[direction][layer].append(message)
            # Now including the original message or a meaningful message in the response
            emit('message_posted', {
                'status': f'Message added to the {layer} layer',
                'direction': direction,
                'layer': layer,
                'message': f'Your message "{message}" has been successfully added.'  # Example of including the original message
            }, broadcast=True)
            app.logger.info(f"Message added to {layer} layer: {message}")
        else:
            emit('error', {'status': 'Invalid direction or layer'})
            app.logger.error('Invalid direction or layer specified in post_message')
    except Exception as e:
        app.logger.error(f"Error handling post_message: {str(e)}")

@socketio.on('get_messages')
def handle_get_messages(data):
    try:
        direction = data['direction']
        layer = data['layer']
        if direction in messages and layer in messages[direction]:
            emit('messages', {'messages': messages[direction][layer], 'direction': direction, 'layer': layer})
            app.logger.info(f"Messages retrieved for {layer} layer")
        else:
            emit('error', {'status': 'Invalid direction or layer'})
            app.logger.error('Invalid direction or layer specified in get_messages')
    except Exception as e:
        app.logger.error(f"Error handling get_messages: {str(e)}")

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
