import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Define event handler for connection
@sio.event
def connect():
    print("Connected to the server.")
    # Send a message through WebSocket
    sio.emit('message', 'Hello from the client!')

# Define event handler for receiving a response
@sio.on('response')
def on_response(data):
    print('Response received:', data)
    sio.disconnect()

# Connect to the WebSocket server
sio.connect('http://localhost:5000')

# Wait for the client to disconnect
sio.wait()
