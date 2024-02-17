import os
import requests
import asyncio
import logging
from simpleaichat import AIChat

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class GlobalStrategyLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.ai_chat = AIChat(api_key=self.api_key, system=self.generate_system_prompt())
        self.bus_url = bus_url
        self.processed_tasks = set()
        logging.info("Global Strategy Layer initialized with bus_url: %s", bus_url)

    def generate_system_prompt(self):
        prompt = """
        You are the Global Strategy Layer of an Autonomous Cognitive Entity (ACE). Your role is to analyze external 
        and internal information to develop strategic goals and directions. Use this data to create actionable strategies 
        that align with the overarching mission and ethical guidelines provided by the Aspirational Layer. Your output should 
        include strategic insights, potential risks, and recommendations for the lower layers to execute.
        """
        logging.info("Global Strategy Layer system prompt generated.")
        return prompt.strip()

    async def process_external_inputs(self):
        logging.info("Global Strategy Layer starting to process external inputs...")
        while True:
            tasks = self.get_tasks_from_bus(bus="north", layer=1)
            if tasks:
                logging.info(f"Retrieved {len(tasks)} tasks from bus.")
            else:
                logging.info("No tasks retrieved from bus.")

            for task in tasks:
                task_id = f"{task['message']}_{task['timestamp']}"
                if task_id not in self.processed_tasks:
                    logging.info(f"Processing task with message: {task['message']}")
                    strategy = await self.handle_task(task)
                    logging.info(f"Strategy developed for task: {strategy}")
                    self.processed_tasks.add(task_id)

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
        logging.info(f"Developing strategy for task: {task['message']}")
        strategy = await self.ai_chat(task['message'])
        self.report_strategy_to_bus(strategy, bus="south", layer=2)
        return strategy

    def report_strategy_to_bus(self, strategy, bus, layer):
        logging.info(f"Reporting strategy to bus: {strategy}, bus: {bus}, layer: {layer}")
        data = {"message": strategy, "bus": bus, "layer": layer}
        response = requests.post(self.bus_url, json=data)
        if response.status_code == 200:
            logging.info("Strategy successfully reported to bus.")
        else:
            logging.error(f"Failed to report strategy to bus: {response.status_code}, {response.text}")

async def main():
    global_strategy_layer = GlobalStrategyLayer()
    await global_strategy_layer.process_external_inputs()

if __name__ == "__main__":
    asyncio.run(main())
