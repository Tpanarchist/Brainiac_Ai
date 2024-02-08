import os
import asyncio
from simpleaichat import AsyncAIChat

class SouthboundBus:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.ai = AsyncAIChat(api_key=self.api_key, system="""
            # Mission
            Your mission is to carry directives and instructions downward through the layers. You allow higher layers to provide guidance, instructions, and objectives to lower layers.
            
            # Instructions
            - Collect directives from upper layers.
            - Ensure these directives are distributed to the correct lower layers based on the intended objectives.
            - Format messages to be clear and actionable for the receiving layers.
            """, console=False)

    async def route_directive(self, input_text):
        # Here, implement logic for routing directives. This is a placeholder.
        response = await self.ai(input_text)
        return response
