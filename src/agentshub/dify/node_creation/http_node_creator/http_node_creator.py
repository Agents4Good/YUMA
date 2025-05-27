from schema.dify import DifyState
from .prompt import HTTP_NODE_CREATOR
from langgraph.types import Command
from models.dify import http_node_creator_model
from agentshub import only_tools_agent
from utils.genia import write_log_state


def http_node_creator(state: DifyState) -> Command:
    _return = only_tools_agent(http_node_creator_model, HTTP_NODE_CREATOR, state)
    write_log_state("http_node_creator - return", _return)
    return _return
