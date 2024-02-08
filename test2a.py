from simpleaichat import AIChat

# Initialize Aspirational_Layer with a system prompt that defines its inspiring and motivational personality.
aspirational_layer = AIChat(system="You are Aspirational_Layer, an inspiring and motivational chatbot designed to help users achieve their dreams and goals.")

# Function to start a continuous chat session with Aspirational_Layer
def start_aspirational_layer_chat():
    print("Aspirational_Layer: Hello! I'm here to inspire and motivate you. What's your dream today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Aspirational_Layer: Remember, every step forward is a step towards achieving something bigger and better. Farewell!")
            break
        response = aspirational_layer(user_input)
        print(f"Aspirational_Layer: {response}")

# Start the chat with Aspirational_Layer
start_aspirational_layer_chat()
