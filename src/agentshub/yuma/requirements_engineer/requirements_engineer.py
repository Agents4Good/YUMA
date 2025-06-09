from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from .prompt import REQUIREMENTS_ENGINEER, REQUIREMENTS_ENGINEER_REFACTED
from typing import Literal
from schema.yuma import AgentState
from models import model_sys
from tools.yuma import make_handoff_tool
from utils.yuma import write_log_state, write_log


requirements_engineer_tool = [make_handoff_tool(agent_name="architecture_agent")]


# Agente reponsável por analisar os requisitos do sistema e conversar com o usuário
def requirements_engineer(
    state: AgentState, 
    max_retries: int = 3,
) -> Command[Literal["human_node", "architecture_agent"]]:
    requirements_engineer_model = create_react_agent(
        model_sys, tools=requirements_engineer_tool, prompt=REQUIREMENTS_ENGINEER_REFACTED
        )
    for attempt in range(max_retries):
        try:
            response = requirements_engineer_model.invoke(state)
            response["active_agent"] = "requirements_engineer"
            
            if isinstance(response['messages'][-2],ToolMessage):
                return Command(update=response,goto='architecture_agent')
            
            _return = Command(update=response, goto="human_node")
            write_log_state("requirements_engineer - return", _return)
            return _return

        except Exception as e:
            if attempt == max_retries - 1:
                write_log(f'requirements_engineer - Falha após várias tentativas', e)
                return Command(update=state, goto="human_node")
