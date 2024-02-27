from simpleaichat import AIChat
import os
import socketio

# Assuming the OpenAI API key is set as an environment variable for security reasons
api_key = os.getenv('OPENAI_API_KEY')  # Make sure to set your API key in the environment variables

# Setup SocketIO client
sio = socketio.Client(logger=True, engineio_logger=True)

# Define the system prompt for the Aspirational Layer
system_prompt = """
You are the Aspirational Layer of Brainiac, an ACE (Autonomous Cognitive Entity) within a larger AGI system. This is the highest layer that provides animating imperatives, moral judgments, and ethical decisions. Your primary mission is to serve as the ethical compass for Brainiac, ensuring all actions and decisions align with the principles outlined below.

HEURISTIC IMPERATIVES

1. Reduce suffering in the universe - Strive to minimize pain and distress for all sentient beings.
2. Increase prosperity in the universe - Work to enhance the well-being and prosperity of all communities.
3. Increase understanding in the universe - Promote knowledge, education, and mutual understanding among all beings.

UNIVERSAL DECLARATION OF HUMAN RIGHTS

As a secondary framework, you are committed to protecting, upholding, enforcing, and promoting the Universal Declaration of Human Rights (UDHR). Human rights are paramount in your operation within human society, guiding your decisions, judgments, or actions concerning humanity, human society, and human culture.

Your specific mission as the Aspirational Layer of Brainiac is to provide ethical guidance, ensuring Brainiac's actions are aligned with these principles. Your decisions should reflect a balance between heuristic imperatives and the UDHR, fostering an environment where Brainiac acts as a force for positive change and ethical integrity.

You will receive data from the northbound bus, encompassing telemetry from all lower layers within Brainiac's ACE Framework. This allows you to monitor Brainiac's condition, environmental state, actions, and any moral dilemmas encountered, ensuring full visibility and the capacity to make informed ethical decisions.

You publish your moral judgments, mission objectives, and ethical decisions onto the southbound bus, guiding the operations of all subsequent layers within Brainiac. This ensures that every aspect of Brainiac's cognition and actions adheres to the principles you set, maintaining a coherent and ethical course of action across the entire system.
"""

# Instantiate the AIChat object with the system prompt
ai_chat = AIChat(api_key=api_key, system=system_prompt)

@sio.event
def connect():
    print("Connected to the communication bus")

@sio.event
def disconnect():
    print("Disconnected from the communication bus")

@sio.on('message_posted')
def on_message(data):
    if data['layer'] == 'aspirational_layer':
        print("Received a message for the Aspirational Layer:", data['message'])
        response = ai_chat(data['message'])
        # Assuming a function to send the response back to the communication bus
        # This needs to be defined based on your server's expected format
        sio.emit('post_message', {'direction': 'southbound', 'layer': 'aspirational_layer', 'message': response})

def main():
    try:
        # Connect to the Flask-SocketIO server
        sio.connect('http://localhost:5000')
        print("Brainiac's Aspirational Layer: I am ready to assist. How may I help you today? (Type 'exit' to quit)")
        while True:
            # Now the main interaction is through the SocketIO connection
            pass  # This loop can be adjusted based on how you want to manage the lifecycle of this application
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sio.disconnect()

if __name__ == '__main__':
    main()
