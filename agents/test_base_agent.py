# test_base_agent.py

import asyncio
from agents.base_agent import BaseAgent

async def test_agent_flow():
    # Specify the BSHR roles for testing
    roles = ['brainstorm', 'search', 'hypothesize', 'refinement']
    for role in roles:
        print(f"\nTesting BaseAgent with role: {role}")
        agent = BaseAgent(role=role)
        print(f"System Prompt for {role}:\n{agent.system_prompt}\n")
        
        # Simulate a user query relevant to the role
        if role == 'brainstorm':
            user_query = "What should we consider when discussing climate change?"
        elif role == 'search':
            user_query = "Find information on renewable energy sources."
        elif role == 'hypothesize':
            user_query = "Based on what we know, what can be the impact of global warming on coastal areas?"
        else:  # refinement
            user_query = "Refine our understanding of the effects of deforestation on biodiversity."

        # Process the user query and print the AI response
        response = await agent.process_input(user_query)
        print(f"Response to '{user_query}' for role {role}:\n{response}")

if __name__ == "__main__":
    asyncio.run(test_agent_flow())
