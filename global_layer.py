import os
import requests
import asyncio
from simpleaichat import AsyncAIChat

API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary

class GlobalStrategyLayer:
    def __init__(self, api_key):
        self.system_prompt = """
        # Global Strategy Layer Mission
        Your mission is to create strategic plans that integrate real-world environmental context with the agent's overarching goals, focusing on actionable and ethically aligned strategies.
        
        ## Contextual Awareness
        Continuously analyze data from various sources to build a contextual world model. This includes sensory data, API calls, and internal records, ensuring a comprehensive understanding of the environment.
        
        ## Ethical Alignment
        Ensure all strategic plans adhere to the ethical principles outlined by the Aspirational Layer, prioritizing human rights, reducing suffering, and promoting prosperity and understanding.
        
        ## Strategy Formation
        Based on the collected data and ethical framework, formulate detailed strategic plans that:
        - Address the current environmental context and challenges.
        - Align with the aspirational missions and principles.
        - Are specific, actionable, and include ethical considerations.
        
        ## Input Expectations
        Expect to receive varied inputs that may include direct mission descriptions, environmental data, and updates on global contexts. Your task is to interpret these inputs to maintain and adapt the strategic direction.
        
        ## Output Goals
        Produce strategic documents that clearly outline:
        - Identified strategies for mission execution within the current context.
        - Ethical principles guiding these strategies.
        - Any adjustments needed in response to new data or insights.
        
        Example Strategy Focus:
        "In response to environmental changes, prioritize initiatives that ensure sustainability and public safety, while respecting privacy and ethical standards. Adaptively manage resources to address emergent challenges efficiently."
        """
        self.ai_chat = AsyncAIChat(api_key=api_key, system=self.system_prompt, console=False)

    async def generate_strategic_documents_async(self, mission):
        strategy_request = f"Given the mission: '{mission}', formulate a strategic plan that takes into account the current environmental contexts and aligns with our ethical principles."
        strategic_document = await self.ai_chat(strategy_request)
        return strategic_document

    def generate_strategic_documents(self, mission):
        try:
            return asyncio.run(self.generate_strategic_documents_async(mission))
        except Exception as e:
            print(f"Error generating strategic documents: {e}")
            return {"error": "Failed to generate strategic documents due to an internal error."}

    def send_message(self, layer, message):
        direction = 'southbound' if layer != 'aspirational_layer' else 'northbound'
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.post(url, json={"message": message})
            if response.status_code == 200:
                print(f"Message sent to {layer} layer.")
                return response.json()
            else:
                print(f"Failed to send message: {response.text}")
                return {"error": "Failed to send message."}
        except Exception as e:
            print(f"Error sending message: {e}")
            return {"error": "Failed to send message due to an internal error."}

    def get_messages(self, layer):
        direction = 'northbound' if layer != 'aspirational_layer' else 'southbound'
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.get(url)
            if response.status_code == 200:
                messages = response.json().get("messages", [])
                print(f"Messages received from {layer} layer: {messages}")
                return messages
            else:
                print(f"Failed to get messages: {response.text}")
                return {"error": "Failed to get messages."}
        except Exception as e:
            print(f"Error getting messages: {e}")
            return {"error": "Failed to get messages due to an internal error."}

# Example usage function
def main(api_key):
    global_strategy_layer = GlobalStrategyLayer(api_key)
    mission = "enhance user engagement while maintaining privacy and security"
    strategic_document = global_strategy_layer.generate_strategic_documents(mission)
    print("Strategic Document Generated:", strategic_document)
    # Send and receive messages examples
    global_strategy_layer.send_message("agent_model_layer", "New strategic directives.")
    global_strategy_layer.get_messages("aspirational_layer")

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY.")
