from .AgentContext import AgentContext
from .DivisionContext import DivisionContext
from .BrainiacContext import BrainiacContext

class ContextManager:
    def __init__(self, base_directory="E:\\Brainiac_Ai\\context\\context_content\\ContextManager"):
        # Ensure the base directories for each context type exist
        self.agent_base_directory = os.path.join(base_directory, "Agent")
        self.division_base_directory = os.path.join(base_directory, "Division")
        self.brainiac_base_directory = os.path.join(base_directory, "Brainiac")

        # Initialize containers for agent and division contexts
        self.agent_contexts = {}
        self.division_contexts = {}
        # Initialize Brainiac context
        self.brainiac_context = BrainiacContext(data_directory=self.brainiac_base_directory, log_directory=os.path.join(self.brainiac_base_directory, "Logs"))

    def get_agent_context(self, agent_id):
        # Dynamically create an agent context if it doesn't exist, within the Agent subdirectory
        if agent_id not in self.agent_contexts:
            agent_dir = os.path.join(self.agent_base_directory, agent_id)
            self.agent_contexts[agent_id] = AgentContext(agent_id=agent_id, base_directory=agent_dir)
        return self.agent_contexts[agent_id]

    def get_division_context(self, division_id):
        # Dynamically create a division context if it doesn't exist, within the Division subdirectory
        if division_id not in self.division_contexts:
            division_dir = os.path.join(self.division_base_directory, division_id)
            self.division_contexts[division_id] = DivisionContext(division_id=division_id, base_directory=division_dir)
        return self.division_contexts[division_id]

    def update_agent_state(self, agent_id, key, value):
        agent_context = self.get_agent_context(agent_id)
        agent_context.update_state(key, value)

    def add_to_division_resources(self, division_id, key, value):
        division_context = self.get_division_context(division_id)
        division_context.update_resource(key, value)

    def log_global_state(self, message):
        self.brainiac_context.add_system_log(message)

# Example usage
context_manager = ContextManager()
context_manager.update_agent_state('agent1', 'status', 'active')
context_manager.add_to_division_resources('global_strategy', 'budget', 100000)
context_manager.log_global_state('System initialized successfully.')