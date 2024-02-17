import os
import logging
import asyncio
from simpleaichat import AIChat
import httpx

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class AspirationalLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.ai = AIChat(api_key=self.api_key, system=self.generate_system_prompt())
        self.bus_url = bus_url
        self.processed_messages = set()
        logging.info("AspirationalLayer initialized with bus_url: %s", bus_url)

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

    async def provide_guidance(self, situation_description):
        logging.info("Providing guidance for: %s", situation_description)
        response = await asyncio.to_thread(self.ai, situation_description)
        logging.info(f"Guidance provided: {response}")
        return response

    async def fetch_and_process_messages(self):
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.get(f"{self.bus_url}?bus=north&layer=0")
                    if response.status_code == 200:
                        messages = response.json().get('messages', [])
                        for message in messages:
                            message_id = f"{message['message']}_{message['timestamp']}"
                            if message_id not in self.processed_messages:
                                logging.info(f"Processing message from bus: {message['message']}")
                                response_text = await self.provide_guidance(message['message'])
                                await self.send_response_to_global_strategy(response_text)
                                self.processed_messages.add(message_id)
                    else:
                        logging.error(f"Failed to fetch messages: {response.status_code}")
                except Exception as e:
                    logging.error(f"Error fetching messages: {e}")
                await asyncio.sleep(5)

    async def send_response_to_global_strategy(self, message):
        async with httpx.AsyncClient() as client:
            try:
                # Sending the response to Global Strategy Layer at layer 1
                response = await client.post(self.bus_url, json={"message": message, "bus": "south", "layer": 1})
                if response.status_code == 200:
                    logging.info("Response sent to Global Strategy Layer successfully.")
                else:
                    logging.error(f"Failed to send response to Global Strategy Layer: {response.status_code}")
            except Exception as e:
                logging.error(f"Error sending response to Global Strategy Layer: {e}")

async def main():
    layer = AspirationalLayer()
    await layer.fetch_and_process_messages()

if __name__ == "__main__":
    asyncio.run(main())
