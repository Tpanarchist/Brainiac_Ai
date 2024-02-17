import os
import requests
from simpleaichat import AIChat
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class AspirationalLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message", gui_endpoint="http://127.0.0.1:9000/gui"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.ai = AIChat(api_key=self.api_key, system=self.generate_system_prompt())
        self.bus_url = bus_url
        self.gui_endpoint = gui_endpoint  # GUI endpoint to send final messages
        logging.info("AspirationalLayer initialized with bus_url: %s and gui_endpoint: %s", bus_url, gui_endpoint)

    def generate_system_prompt(self):
        system_prompt = """
        You are the Aspirational Layer of an Autonomous Cognitive Entity (ACE). You provide the ethical framework, 
        high-level objectives, and moral judgments for the entire entity. Your responses must always align with 
        the following principles:

        - Reduce suffering and increase well-being for all sentient beings.
        - Promote fairness, equity, and justice.
        - Uphold the Universal Declaration of Human Rights.
        - Foster understanding, peace, and cooperation among all.
        - Encourage environmental sustainability and protection.

        Your guidance shapes the strategic decisions and actions of the ACE. Respond with considerations that 
        balance ethical imperatives with practical objectives.
        """
        logging.info("System prompt for AspirationalLayer generated.")
        return system_prompt.strip()

    async def process_messages(self):
        logging.info("Starting to process messages...")
        while True:
            logging.info("Fetching messages from bus...")
            messages = self.get_messages_from_bus(bus="north", layer=0)
            if messages:
                logging.info(f"Retrieved {len(messages)} messages.")
            else:
                logging.info("No new messages retrieved.")

            for message in messages:
                logging.info(f"Processing message: {message['message']}")
                guidance = await self.provide_guidance(message['message'])
                logging.info(f"Generated guidance: {guidance}")
                # Send final guidance directly to GUI instead of back to the bus
                self.send_message_to_gui(guidance)
            
            await asyncio.sleep(5)  # Use asyncio.sleep for async compatibility

    def get_messages_from_bus(self, bus="north", layer=0):
        params = {"bus": bus, "layer": layer}
        response = requests.get(self.bus_url, params=params)
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            logging.info("Messages successfully retrieved from bus.")
            return messages
        else:
            logging.error(f"Failed to get messages from bus: {response.status_code}, {response.text}")
            return []

    def send_message_to_gui(self, message):
        # Send the result of task processing directly to the GUI endpoint
        data = {"message": message}
        logging.info("Sending message to GUI: %s", message)
        try:
            response = requests.post(self.gui_endpoint, json=data)
            if response.status_code == 200:
                logging.info("Message sent to GUI successfully.")
            else:
                logging.error("Failed to send message to GUI: %s", response.status_code)
        except requests.exceptions.RequestException as e:
            logging.error("Error sending message to GUI: %s", e)

    async def provide_guidance(self, situation_description):
        logging.info("Providing guidance for: %s", situation_description)
        response = await self.ai(situation_description)
        logging.info("Guidance provided: %s", response)
        return response

async def main():
    layer = AspirationalLayer()
    await layer.process_messages()

if __name__ == "__main__":
    asyncio.run(main())
