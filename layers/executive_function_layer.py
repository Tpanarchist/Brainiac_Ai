import os
import requests
import asyncio
import logging
from simpleaichat import AIChat

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ExecutiveFunctionLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logging.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.ai_chat = AIChat(api_key=self.api_key, system=self.generate_system_prompt())
        self.bus_url = bus_url
        logging.info("Executive Function Layer initialized with bus URL: %s", bus_url)

    def generate_system_prompt(self):
        prompt = """
        You are the Executive Function Layer of an Autonomous Cognitive Entity (ACE). Your task is to manage resources,
        assess potential risks, and develop detailed project plans based on strategies provided by the Global Strategy Layer.
        Ensure that your plans are feasible, account for all necessary resources, and include risk mitigation strategies.
        """
        logging.info("Executive Function Layer system prompt generated.")
        return prompt.strip()

    async def process_external_inputs(self):
        logging.info("Executive Function Layer starting to process external inputs...")
        while True:
            strategies = self.get_strategies_from_bus(bus="north", layer=3)
            if strategies:
                logging.info(f"Retrieved {len(strategies)} strategies from bus.")
            else:
                logging.info("No strategies retrieved from bus.")

            for strategy in strategies:
                logging.info(f"Developing project plan for strategy: {strategy['message']}")
                project_plan = await self.handle_strategy(strategy)
                logging.info(f"Project plan for strategy reported: {project_plan}")

            await asyncio.sleep(5)

    def get_strategies_from_bus(self, bus, layer):
        logging.info(f"Fetching strategies from bus: {bus}, layer: {layer}")
        params = {"bus": bus, "layer": layer}
        response = requests.get(self.bus_url, params=params)
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            return messages
        else:
            logging.error(f"Failed to fetch strategies from bus: {response.status_code}, {response.text}")
            return []

    async def handle_strategy(self, strategy):
        logging.info(f"Processing strategy: {strategy['message']}")
        project_plan = await self.ai_chat(strategy['message'])
        self.report_project_plan_to_bus(project_plan, bus="south", layer=4)
        return project_plan

    def report_project_plan_to_bus(self, project_plan, bus, layer):
        logging.info(f"Reporting project plan to bus: {project_plan}, bus: {bus}, layer: {layer}")
        data = {"message": project_plan, "bus": bus, "layer": layer}
        response = requests.post(self.bus_url, json=data)
        if response.status_code == 200:
            logging.info("Project plan successfully reported to bus.")
        else:
            logging.error(f"Failed to report project plan to bus: {response.status_code}, {response.text}")

async def main():
    executive_function_layer = ExecutiveFunctionLayer()
    await executive_function_layer.process_external_inputs()

if __name__ == "__main__":
    asyncio.run(main())
