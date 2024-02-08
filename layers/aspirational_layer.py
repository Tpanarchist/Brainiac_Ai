import asyncio
from simpleaichat import AsyncAIChat
from busses.southbound_bus import SouthboundBus    

class AspirationalLayer:
    def __init__(self, api_key, southbound_bus):
        self.southbound_bus = southbound_bus
        # Use AsyncAIChat for asynchronous behavior
        self.agent = AsyncAIChat(api_key=api_key, system="You are the Aspirational Layer responsible for setting the ethical and moral guidelines for the entity.")

    async def send_directive(self, directive):
        # Send directive asynchronously to the global strategy layer
        recipient_layer = "global_strategy_layer"  # Ensure this matches the key used in SouthboundBus's layer_map
        await self.southbound_bus.send_directive(directive, recipient_layer)

# Example usage of the AspirationalLayer
async def main():
    api_key = "OPENAI_API_KEY"  # Replace with your actual API key
    southbound_bus = SouthboundBus(api_key)  # Assuming SouthboundBus is already implemented and imported
    aspirational_layer = AspirationalLayer(api_key, southbound_bus)
    await aspirational_layer.send_directive("Maximize user engagement while adhering to ethical guidelines.")

if __name__ == "__main__":
    asyncio.run(main())
