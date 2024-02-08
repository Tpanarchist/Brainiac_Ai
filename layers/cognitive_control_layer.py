# Cognitive Control Layer
from simpleaichat import AIChat

class CognitiveControlLayer:
    def __init__(self, api_key, southbound_bus, northbound_bus):
        self.southbound_bus = southbound_bus
        self.northbound_bus = northbound_bus
        self.agent = AIChat(api_key=api_key, system="You are the Cognitive Control Layer, selecting and switching tasks dynamically.")

    def select_task(self, task_info):
        print(f"Cognitive Control Layer selecting task with info: {task_info}")
        # Placeholder for task selection logic
