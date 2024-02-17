import os
import requests
import asyncio
import logging
from simpleaichat import AIChat

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CognitiveControlLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logging.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.ai_chat = AIChat(api_key=self.api_key, system=self.generate_system_prompt())
        self.bus_url = bus_url
        logging.info("Cognitive Control Layer initialized with bus URL: %s", bus_url)

    def generate_system_prompt(self):
        prompt = """
        You are the Cognitive Control Layer of an Autonomous Cognitive Entity (ACE). Your role is to dynamically 
        select and switch tasks based on the current environmental conditions and internal state. Use strategic 
        directions and project plans from the upper layers, assess them, and decide on the immediate next actions 
        to take. Ensure your decisions align with the overall mission and objectives of the ACE.
        """
        logging.info("Cognitive Control Layer system prompt generated.")
        return prompt.strip()

    async def process_external_inputs(self):
        logging.info("Cognitive Control Layer starting to process external inputs...")
        while True:
            tasks = self.get_tasks_from_bus(bus="north", layer=4)
            if tasks:
                logging.info(f"Retrieved {len(tasks)} tasks from bus.")
            else:
                logging.info("No tasks retrieved from bus.")

            for task in tasks:
                logging.info(f"Developing decision for task: {task['message']}")
                task_decision = await self.handle_task(task)
                logging.info(f"Decision for task reported: {task_decision}")

            await asyncio.sleep(5)

    def get_tasks_from_bus(self, bus, layer):
        logging.info(f"Fetching tasks from bus: {bus}, layer: {layer}")
        params = {"bus": bus, "layer": layer}
        response = requests.get(self.bus_url, params=params)
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            return messages
        else:
            logging.error(f"Failed to fetch tasks from bus: {response.status_code}, {response.text}")
            return []

    async def handle_task(self, task):
        logging.info(f"Processing task: {task['message']}")
        task_decision = await self.ai_chat(task['message'])
        self.report_decision_to_bus(task_decision, bus="south", layer=5)
        return task_decision

    def report_decision_to_bus(self, decision, bus, layer):
        logging.info(f"Reporting decision to bus: {decision}, bus: {bus}, layer: {layer}")
        data = {"message": decision, "bus": bus, "layer": layer}
        response = requests.post(self.bus_url, json=data)
        if response.status_code == 200:
            logging.info("Decision successfully reported to bus.")
        else:
            logging.error(f"Failed to report decision to bus: {response.status_code}, {response.text}")

async def main():
    cognitive_control_layer = CognitiveControlLayer()
    await cognitive_control_layer.process_external_inputs()

if __name__ == "__main__":
    asyncio.run(main())
