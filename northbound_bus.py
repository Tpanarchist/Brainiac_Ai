import os
import asyncio
from simpleaichat import AsyncAIChat

class NorthboundBus:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.ai = AsyncAIChat(api_key=self.api_key, system="""
            # Mission
            Your mission is to route internal state updates and external sensor data upward through the layers. You enable lower layers to provide telemetry to higher layers.
            
            # Instructions
            - Collect messages from lower layers.
            - Route these messages to the appropriate upper layers based on predefined routing logic.
            - Ensure messages are formatted correctly and contain all necessary information.
            """, console=False)

    async def route_message(self, input_text):
        # Here, implement logic for routing the message. This is a placeholder.
        response = await self.ai(input_text)
        return response
