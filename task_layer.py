import os
import asyncio
import requests
from simpleaichat import AsyncAIChat
import subprocess

API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary

class TaskProsecutionLayer:
    def __init__(self, api_key):
        self.system_prompt = """
            # Mission
            Execute tasks, monitor progress, and detect success or failure based on feedback and monitoring. Realize strategic plans into actions.

            # Context
            Operates within the ACE framework, executing tasks from the Cognitive Control Layer, monitoring real-time feedback and state telemetry.

            # Instructions
            - Execute tasks using provided instructions.
            - Monitor task progress against success/failure criteria.
            - Trigger the next task based on completion status and instructions from above layers.

            # Expected Input
            Detailed task instructions, success/failure criteria, sensor feeds, and internal state telemetry.

            # Output Format
            - Southbound: Actuator commands, digital outputs, environmental interactions.
            - Northbound: Task completion statuses, telemetry, and state updates.
            """
        self.ai_chat = AsyncAIChat(api_key=api_key, system=self.system_prompt, console=False)

    async def execute_task_async(self, task_instructions):
        # Simulate executing a task and monitoring its execution asynchronously
        try:
            # Example: Execute a system command based on the task instructions
            completed_process = subprocess.run(task_instructions['command'], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            response = f"Executed command: {task_instructions['command']}\nOutput:\n{completed_process.stdout}"
            print(f"Task Execution Response:\n{response}")
            return True  # Assuming success if no exception is raised
        except subprocess.CalledProcessError as e:
            print(f"Error executing task: {e}\n{e.stderr}")
            return False

    def execute_task(self, task_instructions):
        try:
            return asyncio.run(self.execute_task_async(task_instructions))
        except Exception as e:
            print(f"Error executing task: {e}")
            return {"error": "Failed to execute task due to an internal error."}

    def send_message(self, direction, layer, message):
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.post(url, json={"message": message})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to send message: {response.text}")
                return {"error": "Failed to send message."}
        except Exception as e:
            print(f"Error sending message: {e}")
            return {"error": "Failed to send message due to an internal error."}

    def get_messages(self, direction, layer):
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("messages", [])
            else:
                print(f"Failed to get messages: {response.text}")
                return {"error": "Failed to get messages."}
        except Exception as e:
            print(f"Error getting messages: {e}")
            return {"error": "Failed to get messages due to an internal error."}

# Example usage
def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        return
    
    task_prosecution_layer = TaskProsecutionLayer(api_key)
    task_instructions = {"command": "dir" if os.name == 'nt' else "ls -l"}
    task_success = task_prosecution_layer.execute_task(task_instructions)
    print("Task Execution Success:", task_success)

if __name__ == "__main__":
    main()
