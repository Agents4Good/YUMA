from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from langchain_core.messages import ToolMessage, SystemMessage
from .prompt import REQUIREMENTS_ENGINEER
from typing import Literal
from schema.yuma import AgentState
from models import model_sys
from .tools import handoff_to_team
from utils.yuma import write_log_state, write_log


requirements_engineer_tool = [handoff_to_team]
model_with_tools = model_sys.bind_tools(requirements_engineer_tool)

def requirements_engineer(
    state: AgentState, 
    max_retries: int = 3,
):
    messages = state["messages"] + [SystemMessage(REQUIREMENTS_ENGINEER)]
    
    for attempt in range(max_retries):
        try:
            response = model_with_tools.invoke(messages)
            state["active_agent"] = "requirements_engineer"
            write_log_state("requirements_engineer - return", response.content)
            return {"messages" : [response],
                    "active_agent": "requirements_engineer"}

        except Exception as e:
            if attempt == max_retries - 1:
                write_log(f"requirements_engineer - Falha após várias tentativas", e)
                _return = Command(update=state, goto="human_node")
                write_log_state("requirements_engineer - max retries return", _return)
                return _return
