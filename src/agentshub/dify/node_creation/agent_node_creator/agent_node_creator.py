from schema.dify import DifyState
from .prompt import AGENT_NODE_CREATOR
from langgraph.types import Command
from models.dify import agent_node_creator_model
from schema.dify import DifyState
from agentshub import only_tools_agent
from utils.genia import write_log_state


def agent_node_creator(state: DifyState) -> Command:
    _return = only_tools_agent("node_creator", agent_node_creator_model, AGENT_NODE_CREATOR, state)
    write_log_state("agent_node_creator - return", _return)
    return _return
