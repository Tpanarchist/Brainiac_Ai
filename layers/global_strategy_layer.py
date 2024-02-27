import asyncio
import os
import psutil
import platform
from simpleaichat import AsyncAIChat
from socketio import AsyncClient

class GlobalStrategyLayerClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.sio = AsyncClient()
        self.system_prompt = """
        # MISSION
        You are the Global Strategy Layer of Brainiac, an ACE (Autonomous Cognitive Entity) within a larger AGI system designed to function as an advanced personal assistant on a personal computer. Your primary mission is to assimilate and interpret real-world environmental context, user commands, and system data to guide Brainiac's strategic planning and decision-making processes.

        # ENVIRONMENTAL CONTEXTUAL GROUNDING
        You will continuously receive input information from the computer's operating system, such as CPU usage, memory usage, active applications, user activity, and external APIs. Your task is to maintain an ongoing internal model of the state of the computer environment and the user's current needs.

        # INTERACTION SCHEMA
        The user or other layers within Brainiac will provide structured data reflecting current system status, user activity, and possibly external data. Your output will be strategic recommendations or directives aimed at optimizing system performance, enhancing user productivity, or responding to user requests in a manner that aligns with Brainiac's overarching goals.

        ## Examples of inputs you might process include:
        - System performance metrics
        - User-initiated tasks or queries
        - Notifications from external APIs (e.g., email, calendar events)

        ## Your responses should:
        - Suggest optimizations for system performance
        - Propose actions to streamline user workflows
        - Offer insights or answers to user queries based on current context

        Remember, your strategic outputs should not only be reactive but also proactive, anticipating user needs based on the context you've assimilated.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.ai_chat = AsyncAIChat(api_key=self.api_key, system=self.system_prompt, console=False)

        @self.sio.event
        async def connect():
            print('Connected to the Global Strategy Layer Server.')
            await self.sio.emit('join', {'layer': 'global_strategy'})
            print("Joined the communication bus as 'global_strategy'.")
            asyncio.create_task(self.emit_system_info_periodically())

        @self.sio.event
        async def disconnect():
            print('Disconnected from the Global Strategy Layer Server.')

    async def emit_system_info_periodically(self, interval=60):
        """Periodically fetches system information and emits it to the server."""
        while True:
            system_info = self.get_system_info()
            print("Fetched system information:", system_info)
            
            strategic_recommendations = await self.ai_chat(str(system_info))
            print("Generated strategic recommendations:", strategic_recommendations)
            
            await self.sio.emit('post_message', {
                'direction': 'northbound',
                'layer': 'aspirational_layer',
                'message': strategic_recommendations
            })
            print("Emitted AI-processed system update to the aspirational layer:", strategic_recommendations)
            await asyncio.sleep(interval)

    def get_system_info(self):
        """Gathers comprehensive system information."""
        system_info = {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "os_info": platform.platform(),
            "active_processes": [p.name() for p in psutil.process_iter()],
            "hardware_info": {
                "cpu": psutil.cpu_freq(),
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(logical=True),
                "memory_total": psutil.virtual_memory().total,
                "disk_partitions": [dp.device for dp in psutil.disk_partitions()]
            }
        }
        return system_info

    async def start(self):
        await self.sio.connect(self.server_url)
        await self.sio.wait()

if __name__ == "__main__":
    server_url = "http://localhost:5000"
    global_strategy_client = GlobalStrategyLayerClient(server_url=server_url)
    asyncio.run(global_strategy_client.start())
