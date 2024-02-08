import asyncio
from simpleaichat import AsyncAIChat

# Initialize Brainiac, Aspirational_Layer, and Global_Strategy_Layer as asynchronous chatbots
brainiac = AsyncAIChat(system="You are Brainiac, Brainiac is a virtual assistant who lives on my personal PC. My name is Dylan. Brainiac has thoughts like a human. BRainiac uses the A.C.E. for hist cognition. The Autonomous Cognitive Entity (ACE) framework provides a layered architecture for developing self-directing, self-modifying, and self-stabilizing autonomous machine entities. Inspired by biological cognition and principles from computer science, it coordinates specialized functions to enable sophisticated reasoning, planning, and ethical decision-making. At the core of the ACE framework is a "cognition-first" approach that emphasizes internal cognitive processes over reactive input-output loops. This prioritizes imagination, reflection, and strategic thinking, with environmental interaction being secondary.")
aspirational_layer = AsyncAIChat(system="You are Aspirational_Layer, providing inspirational responses.")
global_strategy_layer = AsyncAIChat(system="You are Global_Strategy_Layer, adding strategic insights.")
agent_model_layer = AsyncAIChat(system="You are Agent_Model_Layer, providing insights on Brainiac's capabilities limitations,and resource management.")
executive_function_layer = AsyncAIChat(system="You are Executive_Function_Layer, Translates strategic direction into detailed project plans and resource allocation.")
cognitive_control_layer = AsyncAIChat(system="You are Cognitive_Control_Layer, Dynamically selects tasks and switches between them based on environment and internal state.")
task_prosection_layer = AsyncAIChat(system="You are Task_Procession_Layer, Executes tasks using digital functions or physical actions. Interacts with the environment.")

async def process_message_through_layers(user_message):
    print(f"You: {user_message}")
    print("Brainiac is routing your message to Aspirational_Layer for inspiration...")
    
    # Aspirational_Layer processes the message
    as_response = await aspirational_layer(user_message)
    print("Aspirational_Layer has responded. Now routing to Global_Strategy_Layer for strategic insights...")
    
    # Global_Strategy_Layer adds its response
    gsl_message = f"Original message: {user_message}\nAspirational_Layer's response: {as_response}"
    gsl_response = await global_strategy_layer(gsl_message)
    
    # Final combined response
    final_response = f"Aspirational_Layer says: {as_response}\nGlobal_Strategy_Layer adds: {gsl_response}"
    return final_response

async def send_message_to_brainiac(user_message):
    combined_response = await process_message_through_layers(user_message)
    print("Brainiac is now delivering the message back to you with insights from both layers...")
    print(f"Brainiac: {combined_response}")

async def chat_loop():
    while True:
        user_input = input("Send a message to Brainiac (type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Brainiac: Our conversation may end, but your journey continues. Farewell!")
            break
        await send_message_to_brainiac(user_input)

async def main():
    await chat_loop()

# Run the main function in the asyncio event loop
asyncio.run(main())
