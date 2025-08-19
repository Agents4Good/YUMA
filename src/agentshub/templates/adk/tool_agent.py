AGENT_TEMPLATE = '''
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from .tools.tools import {tools}

load_dotenv(override=True)

model = LiteLlm(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL")
)

root_agent = Agent(
    name="{agent_name}",
    model=model,

    instruction="{prompt}",
    tools=[{tools}],
)
'''

TOOL_TEMPLATE = '''
def {tool_name}({params}):
    """
    {description}
  
    {params_doc}
  
    :return: {return_doc}
    """
    {code}
'''