from simpleaichat import AIChat

# Initialize Brainiac with a system prompt that defines its personality and capabilities.
brainiac = AIChat(system="You are Brainiac, a knowledgeable and witty chatbot ready to engage on a wide array of topics.")

# Function to start a continuous chat session
def start_brainiac_chat():
    print("Brainiac: Hello! I am Brainiac. How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Brainiac: Goodbye! Feel free to return if you have more questions.")
            break
        response = brainiac(user_input)
        print(f"Brainiac: {response}")

# Start the chat
start_brainiac_chat()
