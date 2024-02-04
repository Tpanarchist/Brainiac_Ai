import unittest
import os
import json
from .DivisionContext import DivisionContext
  # Ensure this import matches your project structure

class TestDivisionContext(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up directories for testing; these could be temporary directories
        cls.data_directory = "test_data"
        cls.log_directory = "test_logs"
        cls.division_id = "test_division"

    def setUp(self):
        # Initialize DivisionContext with test directories and clean up before each test
        self.division_context = DivisionContext(self.division_id, self.data_directory, self.log_directory)
        self.cleanup()

    def tearDown(self):
        # Clean up test files after each test
        self.cleanup()

    @classmethod
    def tearDownClass(cls):
        # Clean up directories after all tests
        cls.cleanup(cls.data_directory)
        cls.cleanup(cls.log_directory)

    @classmethod
    def cleanup(cls, directory=None):
        # Helper method to remove files created during tests
        if directory and os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

    def test_update_and_log(self):
        # Test updating resources and logging changes
        self.division_context.update_resource('budget', 200000)
        self.division_context.update_task_status('task002', 'in_progress')
        log_path = os.path.join(self.log_directory, f"{self.division_id}_changes.log")

        self.assertTrue(os.path.exists(log_path))
        with open(log_path, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn('Updated resource: budget = 200000', log_contents)
            self.assertIn('Updated task status: task002 = in_progress', log_contents)

    def test_save_and_load_state(self):
        # Test saving and loading the division context state
        self.division_context.update_resource('budget', 300000)
        self.division_context.save_state()
        self.division_context.update_resource('budget', 0)  # Change the budget to check if load works

        self.division_context.load_state()
        self.assertEqual(self.division_context.shared_resources['budget'], 300000)

    def test_serialize_to_text(self):
        # Test serializing the division context to text
        self.division_context.update_resource('equipment', 'computers')
        self.division_context.serialize_to_text()
        text_path = os.path.join(self.log_directory, f"{self.division_id}_context.txt")

        self.assertTrue(os.path.exists(text_path))
        with open(text_path, 'r') as text_file:
            text_contents = text_file.read()
            self.assertIn('equipment', text_contents)
            self.assertIn('computers', text_contents)

if __name__ == '__main__':
    unittest.main()
