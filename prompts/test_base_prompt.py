# test_prompt_loading.py

from base_prompt import BasePrompt

def test_prompt_loading():
    for role in ['brainstorm', 'search', 'hypothesize', 'refinement']:
        print(f"Testing prompt loading for role: {role}")
        prompt = BasePrompt(role)
        print(f"Loaded prompt structure for {role}: {prompt.prompt_structure}")
        print(f"Constructed prompt: {prompt.construct_prompt()}\n")

if __name__ == "__main__":
    test_prompt_loading()
