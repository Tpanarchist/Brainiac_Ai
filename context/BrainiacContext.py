import json
import os
from datetime import datetime

class BrainiacContext:
    def __init__(self, base_directory="E:\\Brainiac_Ai\\context\\context_content\\Brainiac"):
        self.global_state = {}
        self.system_logs = []
        self.data_directory = os.path.join(base_directory, 'Data')
        self.log_directory = os.path.join(base_directory, 'Logs')
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.log_directory, exist_ok=True)

    def update_global_state(self, key, value):
        self.global_state[key] = value
        self.save_global_state()

    def add_system_log(self, message):
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp}: {message}"
        self.system_logs.append(log_entry)
        self.log_system_activity(log_entry)

    def get_global_state(self):
        return self.global_state

    def get_system_logs(self):
        return self.system_logs

    def save_global_state(self):
        path = os.path.join(self.data_directory, "global_state.json")
        with open(path, 'w') as file:
            json.dump(self.global_state, file, indent=4)

    def load_global_state(self):
        path = os.path.join(self.data_directory, "global_state.json")
        if os.path.exists(path):
            with open(path, 'r') as file:
                self.global_state = json.load(file)

    def log_system_activity(self, message):
        log_path = os.path.join(self.log_directory, "system_activity.log")
        with open(log_path, 'a') as log_file:
            log_file.write(message + "\n")

    def load_system_logs(self):
        log_path = os.path.join(self.log_directory, "system_activity.log")
        if os.path.exists(log_path):
            with open(log_path, 'r') as log_file:
                self.system_logs = log_file.read().splitlines()

# Usage example:
brainiac_context = BrainiacContext()
brainiac_context.update_global_state('uptime', '00:10:00')
brainiac_context.add_system_log('System started successfully.')
brainiac_context.save_global_state()
brainiac_context.load_global_state()
brainiac_context.load_system_logs()