import unittest
import requests
import threading
import time
from bus import app as bus_app  # Import the Flask app for the communication bus

class TestBrainiacIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask app for the communication bus in a background thread
        cls.bus_server_thread = threading.Thread(target=lambda: bus_app.run(port=9000, debug=False, use_reloader=False))
        cls.bus_server_thread.daemon = True
        cls.bus_server_thread.start()
        # Wait a moment for the server to start
        time.sleep(1)
    
    def test_send_and_receive_message(self):
        # Simulate sending a message from the GUI to the Aspirational Layer
        message = "Hello, Brainiac!"
        send_response = requests.post('http://127.0.0.1:9000/message', json={"message": message, "bus": "south", "layer": 0})
        
        # Check if the message was sent successfully
        self.assertEqual(send_response.status_code, 200)

        # Poll the communication bus for a response from the Aspirational Layer
        # Note: In a real test, you'd have more sophisticated logic to wait for a response.
        time.sleep(5)  # Wait for the Aspirational Layer to process and respond
        receive_response = requests.get('http://127.0.0.1:9000/message', params={"bus": "north", "layer": 1})
        
        # Check if we received a response
        self.assertEqual(receive_response.status_code, 200)
        messages = receive_response.json().get('messages', [])
        self.assertTrue(len(messages) > 0, "No response received from Brainiac.")
        
        # Optionally, check the content of the response
        # This part depends on the implementation of your Aspirational Layer
        # Example:
        # response_message = messages[0]['message']
        # self.assertIn("response phrase", response_message)

if __name__ == '__main__':
    unittest.main()
