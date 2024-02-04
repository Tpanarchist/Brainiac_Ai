# Let's write a unit test for the AgentContext class with logging capabilities.
# The test will ensure that state and history are accurately recorded and can be reloaded.

import unittest
import os
import json
from unittest.mock import patch

# This is the AgentContext class we're testing.
class AgentContext:
    def __init__(self, agent_id, log_directory="logs"):
        self.agent_id = agent_id
        self.state = {}
        self.history = []
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)

    def update_state(self, key, value):
        self.state[key] = value
        self.log_state()

    def add_to_history(self, message):
        self.history.append(message)
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
        file_path = os.path.join(self.log_directory, f"{self.agent_id}_state.txt")
        with open(file_path, 'w') as file:
            file.write(json.dumps(self.state, indent=4))

    def log_history(self):
        file_path = os.path.join(self.log_directory, f"{self.agent_id}_history.txt")
        with open(file_path, 'w') as file:
            for entry in self.history:
                file.write(f"{entry}\n")

    def load_state(self):
        file_path = os.path.join(self.log_directory, f"{self.agent_id}_state.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.state = json.load(file)

    def load_history(self):
        file_path = os.path.join(self.log_directory, f"{self.agent_id}_history.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.history = file.read().splitlines()

# Here is the unit test for the AgentContext class.
class TestAgentContext(unittest.TestCase):
    def setUp(self):
        self.agent_id = 'test_agent'
        self.context = AgentContext(self.agent_id)
        self.state_key = 'test_state'
        self.state_value = 'value'
        self.message = 'test_message'

    def test_state_logging(self):
        # Update the state and verify it's logged correctly.
        self.context.update_state(self.state_key, self.state_value)
        expected_state = {self.state_key: self.state_value}
        self.assertEqual(self.context.get_state(), expected_state)

        # Verify the state is logged to a file correctly.
        state_file_path = os.path.join(self.context.log_directory, f"{self.agent_id}_state.txt")
        with open(state_file_path, 'r') as file:
            logged_state = json.load(file)
        self.assertEqual(logged_state, expected_state)

    def test_history_logging(self):
        # Add to history and verify it's logged correctly.
        self.context.add_to_history(self.message)
        expected_history = [self.message]
        self.assertEqual(self.context.get_history(), expected_history)

        # Verify the history is logged to a file correctly.
        history_file_path = os.path.join(self.context.log_directory, f"{self.agent_id}_history.txt")
        with open(history_file_path, 'r') as file:
            logged_history = file.read().splitlines()
        self.assertEqual(logged_history, expected_history)

    def tearDown(self):
        # Modify the tearDown method to handle file existence check
        state_file = os.path.join(self.context.log_directory, f"{self.agent_id}_state.txt")
        history_file = os.path.join(self.context.log_directory, f"{self.agent_id}_history.txt")

        if os.path.exists(state_file):
            os.remove(state_file)
        if os.path.exists(history_file):
            os.remove(history_file)

        if os.path.exists(self.context.log_directory):
            os.rmdir(self.context.log_directory)

if __name__ == '__main__':
    unittest.main()

