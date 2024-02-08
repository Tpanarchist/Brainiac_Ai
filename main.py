import os
from layers.aspirational_layer import AspirationalLayer
from layers.global_strategy_layer import GlobalStrategyLayer
from layers.agent_model_layer import AgentModelLayer
from layers.executive_function_layer import ExecutiveFunctionLayer
from layers.cognitive_control_layer import CognitiveControlLayer
from layers.task_prosecution_layer import TaskProsecutionLayer
from busses.northbound_bus import NorthboundBus
from busses.southbound_bus import SouthboundBus

# API Key setup (securely managed via environment variables)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize communication buses as agents
northbound_bus = NorthboundBus(api_key)
southbound_bus = SouthboundBus(api_key)

# Initialize layers with communication buses
aspirational_layer = AspirationalLayer(api_key, southbound_bus)
global_strategy_layer = GlobalStrategyLayer(api_key, southbound_bus, northbound_bus)
agent_model_layer = AgentModelLayer(api_key, southbound_bus, northbound_bus)
executive_function_layer = ExecutiveFunctionLayer(api_key, southbound_bus, northbound_bus)
cognitive_control_layer = CognitiveControlLayer(api_key, southbound_bus, northbound_bus)
task_prosecution_layer = TaskProsecutionLayer(api_key, northbound_bus)

# Orchestration logic
if __name__ == "__main__":
    aspirational_layer.send_directive("Maximize user engagement while adhering to ethical guidelines.")
