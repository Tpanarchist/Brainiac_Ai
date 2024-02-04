import asyncio
import pytest
from agents.base_agent import BaseAgent
from context.ContextManager import ContextManager  # Adjust this import path as needed

# Use a fixture to initialize ContextManager and share it across tests
@pytest.fixture
async def context_manager():
    return ContextManager(base_directory="E:\\Brainiac_Ai\\context\\context_content\\ContextManager")

@pytest.mark.asyncio
async def test_agent_context_flow(context_manager):
    # Define roles, corresponding user queries, and context actions
    roles = ['brainstorm', 'search', 'hypothesize', 'refinement']
    queries = {
        'brainstorm': "What should we consider when discussing climate change?",
        'search': "Find information on renewable energy sources.",
        'hypothesize': "What could be the impact of global warming on coastal areas?",
        'refinement': "Refine our understanding of the effects of deforestation."
    }

    # Iterate through each role, perform context updates, and process queries
    for role in roles:
        print(f"\nTesting role: {role} with context interaction")
        agent = BaseAgent(role=role, api_key='your_api_key_here')  # Ensure you have a valid API key

        # Example context updates
        context_manager.update_agent_state('agent1', 'role', role)
        context_manager.add_to_division_resources('global_strategy', 'budget', 100000)
        context_manager.log_global_state(f"Agent {role} processing started")

        user_query = queries[role]
        print(f"User query: {user_query}")

        # Execute the query and wait for the response
        response = await agent.process_input(user_query)
        print(f"AI Response: {response}")

        # Optionally, inspect context state after processing
        agent_context = context_manager.get_agent_context('agent1')
        division_context = context_manager.get_division_context('global_strategy')
        print(f"Agent state after processing: {agent_context.get_state()}")
        print(f"Division resources after processing: {division_context.get_shared_resources()}")
