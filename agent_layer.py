import asyncio
import os
import requests
import psutil
from simpleaichat import AsyncAIChat

API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary for your Flask app

class AgentModelLayer:
    def __init__(self, api_key):
        # System prompt detailing the layer's functionality
        self.system_prompt = """
        # Mission
        Maintain a comprehensive internal self-model of the agent's capabilities, limitations, configuration, and state, enabling strategic alignment with actual capacities.
        
        # Expected Operations
        - Gather and integrate data to update the self-model.
        - Communicate updates and capabilities to other layers.
        - Adapt strategic directives based on self-assessment.
        """
        self.ai_chat = AsyncAIChat(api_key=api_key, system=self.system_prompt, console=False)

    async def update_self_model_async(self):
        # Asynchronous task simulating the update of the self-model
        system_info = await self.gather_system_info_async()
        update_message = f"Self-model updated with: CPU {system_info['cpu_percent']}%, Memory {system_info['memory_usage']}%, Disk {system_info['disk_usage']}%."
        response = await self.ai_chat(update_message)
        return response

    def update_self_model(self):
        # Synchronous wrapper around the asynchronous self-model update function
        try:
            response = asyncio.run(self.update_self_model_async())
            return response
        except Exception as e:
            print(f"Error updating self-model: {e}")
            return {"error": "Failed to update self-model due to an internal error."}

    def send_message(self, direction, layer, message):
        # Synchronously send a message to another layer via the Flask app
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.post(url, json={"message": message})
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to send message: {response.text}"}
        except Exception as e:
            print(f"Error sending message: {e}")
            return {"error": "Failed to send message due to an internal error."}

    def get_messages(self, direction, layer):
        # Synchronously retrieve messages from another layer via the Flask app
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()["messages"]
            else:
                return {"error": f"Failed to get messages: {response.text}"}
        except Exception as e:
            print(f"Error getting messages: {e}")
            return {"error": "Failed to get messages due to an internal error."}

    async def gather_system_info_async(self):
        # Asynchronous task to gather basic system information
        system_info = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }
        return system_info

# Example usage function
def main(api_key):
    agent_model_layer = AgentModelLayer(api_key)
    self_model_update = agent_model_layer.update_self_model()
    print("Self-Model Update Response:", self_model_update)

    # Example of sending a message to another layer
    send_response = agent_model_layer.send_message("southbound", "cognitive_layer", "Self-model updated successfully.")
    print("Send Message Response:", send_response)

    # Example of retrieving messages from another layer
    messages_received = agent_model_layer.get_messages("northbound", "aspirational_layer")
    print("Messages Received:", messages_received)

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    main(api_key)
