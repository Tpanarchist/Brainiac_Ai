import os
import asyncio
from layers.aspirational_layer import AspirationalLayer
from layers.global_strategy_layer import GlobalStrategyLayer
from layers.northbound_bus import NorthboundBus
from layers.southbound_bus import SouthboundBus

async def main():
    # Initialize layers
    aspirational_layer = AspirationalLayer()
    global_strategy_layer = GlobalStrategyLayer()
    northbound_bus = NorthboundBus()
    southbound_bus = SouthboundBus()

    # Example interaction with the Aspirational Layer
    aspirational_response = await aspirational_layer.chat("Example input requiring ethical guidance.")
    print("Aspirational Layer:", aspirational_response)

    # Pass the response from Aspirational Layer to Global Strategy Layer for further processing
    global_strategy_response = await global_strategy_layer.chat(aspirational_response)
    print("Global Strategy Layer:", global_strategy_response)

    # Example user input to Global Strategy Layer
    user_input = "Current global economic trends and their impact on environmental policies."
    global_strategy_response = await global_strategy_layer.chat(user_input)
    print("Global Strategy Layer:", global_strategy_response)

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())
