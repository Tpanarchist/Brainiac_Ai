import unittest
import os
import json
from .DivisionContext import DivisionContext
  # Ensure this import matches your project structure

class TestDivisionContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_directory = "E:\\Brainiac_Ai\\context\\context_content\\Division"
        cls.division_id = "test_division"
        cls.test_division_context = DivisionContext(cls.division_id, cls.base_directory)

    def setUp(self):
        # Ensure clean slate for each test
        self.test_division_context.shared_resources.clear()
        self.test_division_context.task_statuses.clear()
        self.test_division_context.strategy_plans.clear()
        self.test_division_context.risk_assessments.clear()
        self.test_division_context.capabilities.clear()
        self.test_division_context.environmental_model.clear()
        self.test_division_context.ethical_principles.clear()

    def test_update_and_log_resource(self):
        resource_key = "resource1"
        resource_value = {"amount": 100, "unit": "units"}
        self.test_division_context.update_resource(resource_key, resource_value)
        self.assertIn(resource_key, self.test_division_context.shared_resources)
        self.assertEqual(self.test_division_context.shared_resources[resource_key], resource_value)
        # Verify log file creation and content
        log_path = os.path.join(self.base_directory, self.division_id, 'Logs', f"{self.division_id}_changes.log")
        self.assertTrue(os.path.exists(log_path))
        with open(log_path, 'r') as log_file:
            logs = log_file.readlines()
        self.assertTrue(any(resource_key in log for log in logs))

    def test_save_and_load_state(self):
        self.test_division_context.update_resource("resource2", {"amount": 200, "unit": "widgets"})
        self.test_division_context.save_state()
        # Load state into a new instance to verify
        new_context = DivisionContext(self.division_id, self.base_directory)
        new_context.load_state()
        self.assertEqual(new_context.shared_resources, self.test_division_context.shared_resources)

    

if __name__ == '__main__':
    unittest.main()