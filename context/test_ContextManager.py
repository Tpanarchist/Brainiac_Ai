import unittest
import os
from datetime import datetime
from .ContextManager import ContextManager  # Update this import path based on your project structure

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.base_directory = "E:\\Brainiac_Ai\\context\\context_content\\TestContextManager"
        self.context_manager = ContextManager(base_directory=self.base_directory)
        print(f"Test setup: ContextManager initialized with base directory {self.base_directory}")

    def tearDown(self):
        # Optionally, clean up the directories after tests run
        print("Tearing down test directories...")
        for root, dirs, files in os.walk(self.base_directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
                print(f"Removed file: {os.path.join(root, name)}")
            for name in dirs:
                os.rmdir(os.path.join(root, name))
                print(f"Removed directory: {os.path.join(root, name)}")
        os.rmdir(self.base_directory)
        print("Test directories cleaned up.")

    def test_context_initialization(self):
        # Test if base directories for each context type are created
        self.assertTrue(os.path.exists(self.context_manager.agent_base_directory), "Agent base directory does not exist.")
        self.assertTrue(os.path.exists(self.context_manager.division_base_directory), "Division base directory does not exist.")
        self.assertTrue(os.path.exists(self.context_manager.brainiac_base_directory), "Brainiac base directory does not exist.")
        print("ContextManager initialization test passed.")

    def test_update_agent_state(self):
        agent_id = "agent_test"
        self.context_manager.update_agent_state(agent_id, "status", "active")
        agent_context = self.context_manager.get_agent_context(agent_id)
        self.assertEqual(agent_context.get_state()["status"], "active", "Agent state not updated correctly.")
        print("Agent state update test passed.")

    def test_add_to_division_resources(self):
        division_id = "division_test"
        self.context_manager.add_to_division_resources(division_id, "budget", 100000)
        division_context = self.context_manager.get_division_context(division_id)
        self.assertEqual(division_context.get_shared_resources()["budget"], 100000, "Division resources not updated correctly.")
        print("Division resources update test passed.")

    def test_log_global_state(self):
        message = "Global system test log"
        self.context_manager.log_global_state(message)
        brainiac_context = self.context_manager.brainiac_context
        self.assertTrue(any(message in log for log in brainiac_context.get_system_logs()), "Global log not updated correctly.")
        print("Global state log test passed.")

if __name__ == '__main__':
    unittest.main()
