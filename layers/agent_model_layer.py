import os
import requests
import asyncio
import logging
from simpleaichat import AIChat

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class AgentModelLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logging.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

        self.ai_chat = AIChat(api_key=self.api_key, system=self.generate_system_prompt())
        self.bus_url = bus_url
        logging.info("Agent Model Layer initialized with bus URL: %s", bus_url)

    def generate_system_prompt(self):
        prompt = """
        You are the Agent Model Layer of an Autonomous Cognitive Entity (ACE). Your role is to maintain a comprehensive 
        self-model of the agent's capabilities, limitations, and current state. Use incoming data to update the self-model 
        and provide insights on the agent's operational status, potential enhancements, or modifications required. 
        Ensure your analysis aligns with the strategic objectives set by the higher layers and inform them about any 
        changes or updates to the agent's model.
        """
        logging.info("Agent Model Layer system prompt generated.")
        return prompt.strip()

    async def process_external_inputs(self):
        logging.info("Agent Model Layer starting to process external inputs...")
        while True:
            messages = self.get_messages_from_bus(bus="north", layer=2)
            if messages:
                logging.info(f"Retrieved {len(messages)} messages from bus.")
            else:
                logging.info("No messages retrieved from bus.")

            for message in messages:
                logging.info(f"Updating self-model with message: {message['message']}")
                update_result = await self.update_self_model(message)
                logging.info(f"Self-model update result: {update_result}")

            await asyncio.sleep(5)

    def get_messages_from_bus(self, bus, layer):
        logging.info(f"Fetching messages from bus: {bus}, layer: {layer}")
        params = {"bus": bus, "layer": layer}
        response = requests.get(self.bus_url, params=params)
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            return messages
        else:
            logging.error(f"Failed to fetch messages from bus: {response.status_code}, {response.text}")
            return []

    async def update_self_model(self, message):
        logging.info(f"Processing update for self-model with message: {message['message']}")
        update_result = await self.ai_chat(message['message'])
        self.report_update_to_bus(update_result, bus="south", layer=3)
        return update_result

    def report_update_to_bus(self, update, bus, layer):
        logging.info(f"Reporting self-model update to bus: {update}, bus: {bus}, layer: {layer}")
        data = {"message": update, "bus": bus, "layer": layer}
        response = requests.post(self.bus_url, json=data)
        if response.status_code == 200:
            logging.info("Self-model update successfully reported to bus.")
        else:
            logging.error(f"Failed to report self-model update to bus: {response.status_code}, {response.text}")

async def main():
    agent_model_layer = AgentModelLayer()
    await agent_model_layer.process_external_inputs()

if __name__ == "__main__":
    asyncio.run(main())
