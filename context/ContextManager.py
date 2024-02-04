from AgentContext import AgentContext
from DivisionContext import DivisionContext
from BrainiacContext import BrainiacContext

class ContextManager:
    def __init__(self):
        self.agent_contexts = {agent_id: AgentContext() for agent_id in agents}
        self.division_contexts = {division_name: DivisionContext() for division_name in divisions}
        self.brainiac_context = BrainiacContext()

    # Methods to interact with the different levels of context
    # Example: Update agent state, add to division resources, log to global state, etc.
