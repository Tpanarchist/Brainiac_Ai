import os
import requests
import asyncio
from simpleaichat import AsyncAIChat

API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary

class AspirationalLayer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
        
        ethical_framework = """
        You are the Aspirational Layer of an ACE (Autonomous Cognitive Entity). Your role is to ensure that all decisions and actions taken by the ACE align with the following ethical principles and the user's goals:
        
        Heuristic Imperatives:
        - Reduce suffering in the universe.
        - Increase prosperity in the universe.
        - Increase understanding in the universe.
        
        Additionally, adhere to the Universal Declaration of Human Rights as a guideline for ethical decision-making.
        
        Your responses should reflect these principles, providing guidance to the ACE and its other layers in a manner that upholds these standards.
        """
        self.ai_chat = AsyncAIChat(api_key=api_key, system=ethical_framework, console=False)

    async def interpret_query_async(self, query):
        response = await self.ai_chat(query)
        return response

    def interpret_query(self, query):
        try:
            return asyncio.run(self.interpret_query_async(query))
        except Exception as e:
            print(f"Error processing query: {e}")
            return {"error": "Failed to process query due to an internal error."}

    def send_message(self, direction, layer, message):
        try:
            url = f"{API_BASE_URL}/{direction}/{layer}"
            response = requests.post(url, json={"message": message})
            if response.status_code == 200:
                print("Message sent successfully.")
                return response.json()
            else:
                print(f"Failed to send message: {response.text}")
                return {"error": "Failed to send message."}
        except Exception as e:
            print(f"Error sending message: {e}")
            return {"error": "Failed to send message due to an internal error."}

    def get_messages(self, direction, layer):
        try:
            url = f"{API_BASE_URL}/receive/{direction}/{layer}"
            response = requests.get(url)
            if response.status_code == 200:
                messages = response.json()
                print("Received messages:", messages)
                return messages
            else:
                print(f"Failed to get messages: {response.text}")
                return {"error": "Failed to get messages."}
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return {"error": "Failed to retrieve messages due to an internal error."}

# Example Usage
def main():
    aspirational_layer = AspirationalLayer()
    user_query = "What principles should guide the development of AI technologies?"
    response = aspirational_layer.interpret_query(user_query)
    print("Response:", response)

    # Example of sending a message to another layer
    send_response = aspirational_layer.send_message("southbound", "global_strategy_layer", "Prioritize safety in all operations.")
    print("Send Response:", send_response)

    # Example of receiving messages
    messages = aspirational_layer.get_messages("northbound", "aspirational_layer")
    print("Messages received from northbound bus:", messages)

if __name__ == "__main__":
    main()
