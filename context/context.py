class Context:
    def __init__(self):
        self.conversation_history = []  # Store tuples of (agent_role, message)
        self.task_progress = {}  # Key: TaskID, Value: Progress details
        self.agent_roles = {}  # Key: AgentID, Value: Role
        self.agent_hierarchy = {}  # Key: Role, Value: List of AgentIDs in rank order
        self.session_data = {}  # Miscellaneous session-specific data

    def add_conversation_entry(self, agent_role, message):
        self.conversation_history.append((agent_role, message))

    def update_task_progress(self, task_id, progress):
        self.task_progress[task_id] = progress

    def set_agent_role(self, agent_id, role):
        self.agent_roles[agent_id] = role

    def update_agent_hierarchy(self, role, agent_id_list):
        self.agent_hierarchy[role] = agent_id_list

    def update_session_data(self, key, value):
        self.session_data[key] = value

    # Add more functions as necessary for managing context
class ContextManager:
    def __init__(self):
        self.current_context = Context()

    def update_context_with_message(self, agent_id, agent_role, message):
        self.current_context.add_conversation_entry(agent_role, message)
        # Ensure the agent's role is up-to-date
        if agent_id not in self.current_context.agent_roles or self.current_context.agent_roles[agent_id] != agent_role:
            self.current_context.set_agent_role(agent_id, agent_role)

    def track_task_progress(self, task_id, progress):
        self.current_context.update_task_progress(task_id, progress)

    def register_agent_hierarchy(self, role, agent_id_list):
        self.current_context.update_agent_hierarchy(role, agent_id_list)

    def get_context(self):
        return self.current_context

    def reset_context(self):
        self.current_context = Context()

    # Implement persistence methods if necessary
