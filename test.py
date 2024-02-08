import os
import asyncio
from simpleaichat import AIChat
from typing import Callable, Dict

# Assuming your API key is stored in an environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

# Directory to store dynamically created tools
TOOLS_DIR = "tools"
if not os.path.exists(TOOLS_DIR):
    os.makedirs(TOOLS_DIR)

# Placeholder for storing tool functions dynamically
tools: Dict[str, Callable] = {}

async def create_tool(name: str, code: str):
    """
    Create a tool with the given name and code, and save it to the tools directory.
    This function is a placeholder and does not execute or dynamically load code for security reasons.
    """
    # For demonstration: save the code to a file in the TOOLS_DIR
    filepath = os.path.join(TOOLS_DIR, f"{name}.py")
    with open(filepath, "w") as file:
        file.write(code)
    print(f"Tool saved to {filepath}")

    # Here you would dynamically load the tool into the `tools` dictionary if executing code dynamically was safe
    # For this example, we'll simply log the creation
    print(f"Tool {name} created and loaded.")

async def use_tool(tool_name: str, *args, **kwargs):
    """
    Use a tool by its name with provided arguments.
    This function is a placeholder for demonstrating the concept.
    """
    if tool_name in tools:
        # Dynamically call the tool function from the `tools` dictionary
        result = await tools[tool_name](*args, **kwargs)
        return result
    else:
        raise ValueError(f"Tool {tool_name} not found.")

async def chat_with_agent():
    ai_chat = AIChat(api_key=API_KEY, console=False)

    # Example interaction
    response = await ai_chat("Hello, AI!")  # Starting a conversation
    print(response)

    # Dynamically creating a tool based on interaction (placeholder)
    await create_tool("example_tool", "# Example Python code")

    # Using a dynamically created tool (placeholder)
    try:
        result = await use_tool("example_tool", arg1="value1")
        print(result)
    except ValueError as e:
        print(e)

# Run the main chat function
if __name__ == "__main__":
    asyncio.run(chat_with_agent())
