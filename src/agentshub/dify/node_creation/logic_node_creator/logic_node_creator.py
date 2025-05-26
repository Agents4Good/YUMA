from schema.dify import DifyState
from .prompt import LOGIC_NODE_CREATOR
from langgraph.types import Command
from models.dify import logic_node_creator_model
from agentshub import only_tools_agent
from utils.genia import write_log_state


def logic_node_creator(state: DifyState) -> Command:
    _return = only_tools_agent(logic_node_creator_model, LOGIC_NODE_CREATOR, state)
    write_log_state("logic_node_creator - return", _return)
    return _return
