from schema.dify import DifyState
from langgraph.types import Command
from .prompt import EDGE_CREATOR
from models.dify import edge_creator_dify_model
from agentshub import only_tools_agent
from langchain_core.messages import SystemMessage
from utils.yuma import write_log_state


# Agente responsável por criar as edges do sistema
def edge_creator(state: DifyState) -> Command:
    _return = only_tools_agent(edge_creator_dify_model, [SystemMessage(content=EDGE_CREATOR)], state)
    write_log_state("edge_creator - return", _return)
    return _return
