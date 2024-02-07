import os
import asyncio
from simpleaichat import AsyncAIChat

# Define layer names for easy reference
layer_names = {
    "aspirational": "Aspirational Layer",
    "strategy": "Global Strategy Layer",
    "model": "Agent Model Layer",
    "executive": "Executive Function Layer",
    "cognitive": "Cognitive Control Layer",
    "task": "Task Prosecution Layer",
}

# Function to asynchronously initialize the layers of the ACE framework
async def initialize_layers(api_key):
    return {
        "aspirational": AsyncAIChat(api_key=api_key, system="You are the Aspirational Layer, providing ethical guidance."),
        "strategy": AsyncAIChat(api_key=api_key, system="You are the Global Strategy Layer. Formulate strategic plans based on the environmental context and aspirational goals."),
        "model": AsyncAIChat(api_key=api_key, system="You are the Agent Model Layer. Understand and communicate the agent's capabilities and limitations."),
        "executive": AsyncAIChat(api_key=api_key, system="You are the Executive Function Layer. Create detailed project plans and manage resources."),
        "cognitive": AsyncAIChat(api_key=api_key, system="You are the Cognitive Control Layer. Dynamically select and switch tasks based on current priorities."),
        "task": AsyncAIChat(api_key=api_key, system="You are the Task Prosecution Layer. Execute tasks and interact with the environment."),
    }

# Asynchronous message passing function between layers
async def pass_message_async(sender_id, receiver_id, message, layers):
    sender_name = layer_names[sender_id]
    receiver_name = layer_names[receiver_id]
    receiver = layers[receiver_id]
    print(f"Async message from {sender_name} to {receiver_name}: '{message}'")
    response = await receiver(message)  # Use await to send the message asynchronously
    print(f"Async response from {receiver_name}: '{response}'")
    return response

# Demonstrate asynchronous communication with manual layer names
async def demonstrate_async_communication(layers):
    goal_message = "Maximize environmental sustainability."
    await pass_message_async("aspirational", "strategy", goal_message, layers)

# Main coroutine to run the demonstration
async def main(api_key):
    layers = await initialize_layers(api_key)
    await demonstrate_async_communication(layers)

if __name__ == "__main__":
    # Retrieve the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    asyncio.run(main(api_key))
