import os
import asyncio
import requests
from simpleaichat import AsyncAIChat

API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary

class CognitiveControlLayer:
    def __init__(self, api_key):
        self.system_prompt = """
            # Mission
            The mission of the Cognitive Control Layer is to dynamically switch and select tasks based on environmental conditions and progress toward goals. It ensures that tasks are chosen and executed in an optimal sequence to maximize goal achievement.
            
            # Context
            Operates within the ACE framework, making real-time decisions about task selection and switching based on inputs from upper layers and continuous environmental monitoring.
            
            # Instructions
            - Track progress through project plans, monitor environmental conditions, and internal state for task switching and selection.
            - Prioritize tasks aligning with goal achievement and follow dependencies and criteria for execution.
            - Adapt to changing conditions by executing dynamic task switching when necessary.
            
            # Expected Input
            Project plans, environmental sensor telemetry, internal state data, task completion status, and strategic objectives.
            
            # Output Format
            Clear communication of task instructions, status updates, and real-time decision-making to facilitate task execution.
            """
        self.ai_chat = AsyncAIChat(api_key=api_key, system=self.system_prompt, console=False)

    async def evaluate_environment_and_plan_async(self, environmental_data, project_plan):
        analysis_result = await self.ai_chat(f"Given environmental conditions: {environmental_data} and project plan: {project_plan}, determine the next best task.")
        return analysis_result

    def evaluate_environment_and_plan(self, environmental_data, project_plan):
        try:
            return asyncio.run(self.evaluate_environment_and_plan_async(environmental_data, project_plan))
        except Exception as e:
            print(f"Error in environment evaluation and planning: {e}")
            return {"error": "Failed to evaluate environment and plan due to an internal error."}

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
    
    cognitive_control_layer = CognitiveControlLayer(api_key)
    environmental_data = "Normal operation conditions with a slight increase in user requests."
    project_plan = "Project Plan XYZ including task sequences and resource allocation."
    decision = cognitive_control_layer.evaluate_environment_and_plan(environmental_data, project_plan)
    print("Decision on next task:", decision)

if __name__ == "__main__":
    main()
