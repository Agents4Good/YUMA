from schema.dify import DifyState
from .prompt import START_NODE_CREATOR
from langgraph.types import Command
from models.dify import start_node_creator_model
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot
from utils.yuma import write_log_state


def start_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(archictecure, START_NODE_CREATOR, EXAMPLES, "START")
    _return = only_tools_agent(start_node_creator_model, state["messages"] + new_messages)
    write_log_state("start_node_creator - return", _return)
    return _return
