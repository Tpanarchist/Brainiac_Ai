import os
import asyncio
import requests
from simpleaichat import AsyncAIChat

API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary

class ExecutiveFunctionLayer:
    def __init__(self, api_key):
        self.system_prompt = """
            # Mission
            The mission of the Executive Function Layer is to translate high-level strategic direction into detailed and achievable execution plans, focusing on managing resources and assessing potential risks.

            # Context
            Operates within the ACE framework, developing execution plans aligned with strategic objectives, while monitoring resource availability and assessing risks.

            # Instructions
            - Develop execution plans utilizing capabilities and resources.
            - Monitor real-time environmental telemetry and resource databases.
            - Create detailed project plans with workflows, resource allocation, and risk mitigation.
            - Continuously assess risks and adapt plans accordingly.

            # Expected Input
            Strategic objectives, agent capabilities, environmental telemetry, resource databases.

            # Output Format
            Structured formats for clear execution, including detailed project plans and risk assessments.
            """
        self.ai_chat = AsyncAIChat(api_key=api_key, system=self.system_prompt, console=False)

    async def generate_execution_plan_async(self, strategic_objectives):
        execution_plan_request = f"Develop an execution plan based on: {strategic_objectives}"
        execution_plan = await self.ai_chat(execution_plan_request)
        return execution_plan

    def generate_execution_plan(self, strategic_objectives):
        try:
            return asyncio.run(self.generate_execution_plan_async(strategic_objectives))
        except Exception as e:
            print(f"Error generating execution plan: {e}")
            return {"error": "Failed to generate execution plan due to an internal error."}

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

# Example usage function
def main(api_key):
    executive_function_layer = ExecutiveFunctionLayer(api_key)
    strategic_objectives = "Optimize resource allocation for Project X with an emphasis on risk mitigation."
    execution_plan = executive_function_layer.generate_execution_plan(strategic_objectives)
    print("Execution Plan Generated:", execution_plan)

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    main(api_key)
