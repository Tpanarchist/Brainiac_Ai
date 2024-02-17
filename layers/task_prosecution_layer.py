import os
import requests
from simpleaichat import AIChat
import asyncio
import time
import logging

# Configure logging with more detail
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TaskProsecutionLayer:
    def __init__(self, bus_url="http://127.0.0.1:9000/message"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logging.error("OpenAI API key not found. Setting OPENAI_API_KEY environment variable is required.")
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.ai_chat = AIChat(api_key=self.api_key, system="You are the Task Prosecution Layer of an Autonomous Cognitive Entity (ACE). Execute tasks based on inputs from the bus and report the results back.")
        self.bus_url = bus_url
        logging.info("Task Prosecution Layer initialized with bus URL: %s", bus_url)
        print("Task Prosecution Layer initialized.")

    async def process_external_inputs(self):
        logging.info("Processing external inputs started.")
        print("Processing external inputs...")
        while True:
            logging.info("Fetching tasks from bus...")
            print("Fetching tasks...")
            tasks = self.get_tasks_from_bus()
            if tasks:
                logging.info(f"Found {len(tasks)} tasks.")
                print(f"Found {len(tasks)} tasks.")
                for task in tasks:
                    logging.info(f"Processing task: {task['message']}")
                    print(f"Processing task: {task['message']}")
                    task_result = await self.ai_chat(task['message'])
                    logging.info(f"Task result: {task_result}")
                    print(f"Task result: {task_result}")
                    self.send_result_to_bus(task_result, task['message'])
            else:
                logging.info("No new tasks found.")
                print("No new tasks.")
            await asyncio.sleep(5)

    def get_tasks_from_bus(self):
        logging.info("Retrieving tasks from the bus...")
        response = requests.get(self.bus_url, params={"bus": "north", "layer": 5})
        if response.status_code == 200:
            tasks = response.json().get('messages', [])
            logging.info(f"Retrieved {len(tasks)} tasks from bus.")
            return tasks
        else:
            logging.error("Error fetching tasks from bus: %s", response.status_code)
            print("Failed to fetch tasks from bus.")
            return []

    def send_result_to_bus(self, result, original_message):
        logging.info(f"Sending result back to bus for task: {original_message}")
        print(f"Sending result back to bus for task: {original_message}")
        data = {"message": result, "original": original_message, "bus": "north", "layer": 5}
        response = requests.post(self.bus_url, json=data)
        if response.status_code == 200:
            logging.info("Result successfully sent to bus.")
            print("Result sent to bus successfully.")
        else:
            logging.error("Failed to send result to bus: %s", response.status_code)
            print("Failed to send result to bus.")

async def main():
    task_prosecution_layer = TaskProsecutionLayer()
    await task_prosecution_layer.process_external_inputs()

if __name__ == "__main__":
    asyncio.run(main())
