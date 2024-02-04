# prompts/base_prompt.py
import json
import os

class BasePrompt:
    def __init__(self, role):
        self.role = role
        self.prompt_structure = self.load_prompt_structure()

    def load_prompt_structure(self):
        """
        Dynamically load the prompt structure from an external JSON file
        based on the agent's role.
        """
        prompt_file_path = os.path.join('prompts', f'{self.role}_agent_prompt.json')
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as file:
                prompt_structure = json.load(file)
            return prompt_structure
        except FileNotFoundError:
            # Fallback to a default prompt structure if no specific file is found for the role
            print(f"No prompt file found for role {self.role}. Using default structure.")
            return {
                'Mission': "Provide general assistance.",
                'Context': "Handling a variety of inquiries.",
                'Rules': "Ensure responses are accurate and helpful.",
                'Instructions': "Engage in informative and polite conversation.",
                'Expected Input': "Any general question.",
                'Output Format': "Plain text.",
                'Example Output': "I'm here to help answer your questions."
            }

    def construct_prompt(self):
        """
        Combine elements of the prompt structure into a single prompt string.
        """
        # Combine all elements of the prompt structure to form the system prompt.
        # This could also be tailored to suit specific formatting requirements.
        return "\n".join(f"{key}: {value}" for key, value in self.prompt_structure.items())
