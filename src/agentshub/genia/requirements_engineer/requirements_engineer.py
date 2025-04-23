from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from .prompt import REQUIREMENTS_ENGINEER
from typing import Literal
from schema.genia import AgentState
from models import model
from tools.genia import make_handoff_tool


requirements_engineer_tool = [make_handoff_tool(agent_name="architecture_agent")]


# Agente reponsável por analisar os requisitos do sistema e conversar com o usuário
def requirements_engineer(
    state: AgentState,
) -> Command[Literal["human_node", "architecture_agent"]]:
    system_prompt = REQUIREMENTS_ENGINEER
    requirements_engineer_model = create_react_agent(
        model, tools=requirements_engineer_tool, prompt=system_prompt
    )
    response = requirements_engineer_model.invoke(state)
    response["active_agent"] = "requirements_engineer"
    return Command(update=response, goto="human_node")