import unittest
from unittest.mock import MagicMock, patch
from l1 import AspirationalLayer

class TestAspirationalLayer(unittest.TestCase):
    def setUp(self):
        self.aspirational_layer = AspirationalLayer()

    def test_generate_system_prompt(self):
        expected_prompt = """
        You are the Aspirational Layer of an Autonomous Cognitive Entity (ACE). You provide the ethical framework, 
        high-level objectives, and moral judgments for the entire entity. Your responses must always align with 
        the following principles:

        - Reduce suffering and increase well-being for all sentient beings.
        - Promote fairness, equity, and justice.
        - Uphold the Universal Declaration of Human Rights.
        - Foster understanding, peace, and cooperation among all.
        - Encourage environmental sustainability and protection.

        Your guidance shapes the strategic decisions and actions of the ACE. Respond with considerations that 
        balance ethical imperatives with practical objectives.
        """

        system_prompt = self.aspirational_layer.generate_system_prompt()
        self.assertEqual(system_prompt.strip(), expected_prompt.strip())

    @patch('requests.AsyncClient')
    async def test_get_messages_from_bus(self, mock_async_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'messages': ['message1', 'message2']}
        mock_async_client.return_value.__aenter__.return_value.get.return_value = mock_response

        messages = await self.aspirational_layer.get_messages_from_bus(bus="north", layer=0)
        self.assertEqual(messages, ['message1', 'message2'])

    @patch('requests.AsyncClient')
    async def test_send_message_to_gui(self, mock_async_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_async_client.return_value.__aenter__.return_value.post.return_value = mock_response

        await self.aspirational_layer.send_message_to_gui("Test message")
        mock_async_client.return_value.__aenter__.return_value.post.assert_called_once_with(
            self.aspirational_layer.gui_endpoint, json={"message": "Test message"}
        )

    @patch('asyncio.to_thread')
    async def test_provide_guidance(self, mock_to_thread):
        mock_to_thread.return_value = "Test guidance"

        guidance = await self.aspirational_layer.provide_guidance("Test situation")
        self.assertEqual(guidance, "Test guidance")

if __name__ == '__main__':
    unittest.main()