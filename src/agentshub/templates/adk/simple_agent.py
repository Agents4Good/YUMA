CONVERSATIONAL_AGENT_TEMPLATE = '''
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support

load_dotenv(override=True)

model = LiteLlm(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL")
)

root_agent = Agent(
    name="{agent_name}",
    model=model,
    description="{description}",
    instruction="{prompt}",
)

'''
