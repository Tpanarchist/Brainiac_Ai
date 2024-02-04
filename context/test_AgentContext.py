import unittest
import os
import json
from datetime import datetime
from .AgentContext import AgentContext  # Ensure correct import based on your project structure

class TestAgentContext(unittest.TestCase):
    def setUp(self):
        self.agent_id = 'test_agent'
        self.base_directory = "E:\\Brainiac_Ai\\context\\context_content\\Agent"
        self.data_directory = os.path.join(self.base_directory, 'Data')
        self.log_directory = os.path.join(self.base_directory, 'Logs')
        # Ensure the directories exist
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.log_directory, exist_ok=True)
        # Initialize the AgentContext with the test directories
        self.agent_context = AgentContext(self.agent_id, base_directory=self.base_directory)

    def test_initialization(self):
        # Check that directories exist after initialization
        self.assertTrue(os.path.exists(self.agent_context.data_directory))
        self.assertTrue(os.path.exists(self.agent_context.log_directory))

    def test_update_state_and_log_history(self):
        # Test updating the state and adding a log entry
        self.agent_context.update_state('status', 'active')
        self.agent_context.add_to_history('Agent activated')
        self.assertEqual(self.agent_context.get_state()['status'], 'active')
        self.assertTrue(any('Agent activated' in log for log in self.agent_context.get_history()))

    def test_save_and_load_state(self):
        # Test saving and loading the state
        self.agent_context.update_state('status', 'active')
        self.agent_context.log_state()
        self.agent_context.load_state()
        self.assertEqual(self.agent_context.get_state()['status'], 'active')

    def test_save_and_load_history(self):
        # Test saving and loading the history
        self.agent_context.add_to_history('Agent activated')
        self.agent_context.log_history()
        self.agent_context.load_history()
        self.assertTrue(any('Agent activated' in log for log in self.agent_context.get_history()))

if __name__ == '__main__':
    unittest.main()
