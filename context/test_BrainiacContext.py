import unittest
import os
import json
from datetime import datetime
from .BrainiacContext import BrainiacContext

class TestBrainiacContext(unittest.TestCase):
    def setUp(self):
        # Define the base directory for the test
        self.base_directory = "E:\\Brainiac_Ai\\context\\context_content\\Brainiac"
        self.data_directory = os.path.join(self.base_directory, 'Data')
        self.log_directory = os.path.join(self.base_directory, 'Logs')
        # Ensure the directories exist
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.log_directory, exist_ok=True)
        # Initialize the BrainiacContext with the test directories
        self.brainiac_context = BrainiacContext(base_directory=self.base_directory)

    def test_initialization(self):
        # Check that directories exist after initialization
        self.assertTrue(os.path.exists(self.brainiac_context.data_directory))
        self.assertTrue(os.path.exists(self.brainiac_context.log_directory))

    def test_update_global_state(self):
        # Test updating the global state
        key, value = 'test_key', 'test_value'
        self.brainiac_context.update_global_state(key, value)
        self.assertEqual(self.brainiac_context.global_state[key], value)

    def test_add_system_log(self):
        # Test adding a system log
        message = 'Test log message'
        self.brainiac_context.add_system_log(message)
        # Check that the message with a timestamp is in system logs
        self.assertTrue(any(message in log for log in self.brainiac_context.system_logs))

    def test_save_and_load_global_state(self):
        # Test saving and loading the global state
        self.brainiac_context.update_global_state('test_key', 'test_value')
        self.brainiac_context.save_global_state()
        # Create a new context to load the state
        new_context = BrainiacContext(base_directory=self.base_directory)
        new_context.load_global_state()
        self.assertEqual(new_context.global_state, self.brainiac_context.global_state)

    def test_save_and_load_system_logs(self):
        # Test saving and loading system logs
        message = 'Test log message'
        self.brainiac_context.add_system_log(message)
        # Create a new context to load the logs
        new_context = BrainiacContext(base_directory=self.base_directory)
        new_context.load_system_logs()
        self.assertTrue(any(message in log for log in new_context.system_logs))

if __name__ == '__main__':
    unittest.main()