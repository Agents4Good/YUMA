from langgraph.types import Command
from langchain_core.messages import SystemMessage
from .prompt import REQUIREMENTS_ENGINEER
from typing import Literal
from schema.yuma import AgentState
from models import model_sys
from utils.yuma import write_log_state, write_log
from tools.yuma import handoff_to_agent

engineer_tools = [handoff_to_agent]
engineer_model = model_sys.bind_tools(engineer_tools)

# Agente reponsável por analisar os requisitos do sistema e conversar com o usuário
def requirements_engineer(
    state: AgentState, 
    max_retries: int = 3,
) -> Command[Literal["human_node", "architecture_agent"]]:
    for attempt in range(max_retries):
        try:
            messages = (state["messages"] + 
                        [SystemMessage(content=REQUIREMENTS_ENGINEER)] + 
                        state["human_inputs"])
            response = engineer_model.invoke(messages)
            
            if hasattr(response, "tool_calls") and response.tool_calls:
                _return = Command(update={
                    "messages": state["messages"] + [response],
                    "active_agent": "requirements_engineer",
                    "agente_name": "Engenheiro de Requisitos"
                },
                    goto="engineer_tools")
            else: 
                _return = Command(update={
                                            "messages": state["messages"] + [response],
                                            "active_agent": "requirements_engineer",
                                            "agente_name": "Engenheiro de Requisitos"
                                        },
                                goto="human_node")
                
            write_log_state("requirements_engineer - return", _return)
            return _return

        except Exception as e:
            if attempt == max_retries - 1:
                write_log(f"requirements_engineer - Falha após várias tentativas", e)
                _return = Command(update=state, goto="human_node")
                write_log_state("requirements_engineer - max retries return", _return)
                return _return
