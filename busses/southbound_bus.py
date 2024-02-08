import asyncio
from simpleaichat import AsyncAIChat

# Placeholder imports - replace these with actual layer classes
from layers.aspirational_layer import AspirationalLayer
from layers.global_strategy_layer import GlobalStrategyLayer
from layers.agent_model_layer import AgentModelLayer
from layers.executive_function_layer import ExecutiveFunctionLayer
from layers.cognitive_control_layer import CognitiveControlLayer
from layers.task_prosecution_layer import TaskProsecutionLayer

class SouthboundBus:
    def __init__(self, api_key):
        self.agent = AsyncAIChat(api_key=api_key, system="You are the Southbound Bus responsible for routing directives downwards to the appropriate layers.")
        self.layer_map = {
            'aspirational_layer': AspirationalLayer(api_key),
            'global_strategy_layer': GlobalStrategyLayer(api_key),
            'agent_model_layer': AgentModelLayer(api_key),
            'executive_function_layer': ExecutiveFunctionLayer(api_key),
            'cognitive_control_layer': CognitiveControlLayer(api_key),
            'task_prosecution_layer': TaskProsecutionLayer(api_key)
        }

    async def send_directive(self, directive, layer_name):
        if layer_name in self.layer_map:
            layer = self.layer_map[layer_name]
            # Assuming the layers also have an asynchronous receive_directive method
            await layer.receive_directive(directive)
            print(f"Directive '{directive}' sent to {layer_name} layer.")
        else:
            print(f"Layer '{layer_name}' not recognized.")

    def register_layer(self, layer_name, layer_obj):
        self.layer_map[layer_name] = layer_obj

# Example usage
async def main():
    api_key = "OPENAI_API_KEY"  # Replace with your actual API key
    bus = SouthboundBus(api_key)
    await bus.send_directive("Your directive here", "global_strategy")

if __name__ == "__main__":
    asyncio.run(main())
