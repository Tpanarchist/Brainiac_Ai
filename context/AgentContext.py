import json
import os
from datetime import datetime

class AgentContext:
    def __init__(self, agent_id, base_directory="E:\\Brainiac_Ai\\context\\context_content\\Agent"):
        self.agent_id = agent_id
        self.state = {}
        self.history = []
        self.data_directory = os.path.join(base_directory, 'Data')
        self.log_directory = os.path.join(base_directory, 'Logs')
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.log_directory, exist_ok=True)

    def update_state(self, key, value):
        self.state[key] = value
        self.log_state()

    def add_to_history(self, message):
        timestamped_message = f"{datetime.now().isoformat()} - {message}"
        self.history.append(timestamped_message)
        self.log_history()

    def get_state(self):
        return self.state

    def get_history(self):
        return self.history

    def reset(self):
        self.state.clear()
        self.history.clear()
        self.log_state()
        self.log_history()

    def log_state(self):
        file_path = os.path.join(self.data_directory, f"{self.agent_id}_state.json")
        with open(file_path, 'w') as file:
            file.write(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'state': self.state
            }, indent=4))

    def log_history(self):
        file_path = os.path.join(self.log_directory, f"{self.agent_id}_history.txt")
        with open(file_path, 'a') as file:
            for entry in self.history:
                file.write(f"{entry}\n")

    def load_state(self):
        file_path = os.path.join(self.data_directory, f"{self.agent_id}_state.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
                self.state = loaded_data.get('state', {})

    def load_history(self):
        file_path = os.path.join(self.log_directory, f"{self.agent_id}_history.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.history = file.read().splitlines()

# Usage example:
agent_context = AgentContext('agent1')
agent_context.update_state('status', 'active')
agent_context.add_to_history('Agent activated')
