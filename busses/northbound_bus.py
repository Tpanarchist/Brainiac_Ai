# Northbound bus implementation using simpleaichat

from simpleaichat import AIChat

class NorthboundBus:
    def __init__(self, api_key):
        # The system prompt here can be tailored to the responsibilities of the bus
        self.agent = AIChat(api_key=api_key, system="You are the Northbound Bus responsible for routing messages upwards.")

    def route_message(self, message, recipient_layer_class):
        # Example method to route a message to a specific layer
        print(f"Northbound message for {recipient_layer_class.__name__}: {message}")
        # Logic to send the message to the recipient layer
        # In a real implementation, we would call a method on the recipient layer object
