from schema.dify import DifyState
from .prompt import AGENT_NODE_CREATOR
from langgraph.types import Command
from models.dify import agent_node_creator_model
from schema.dify import DifyState
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot
from utils.yuma import write_log_state


def agent_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(archictecure, AGENT_NODE_CREATOR, EXAMPLES, "AGENTE")
    _return = only_tools_agent(agent_node_creator_model, state["messages"] + new_messages)
    write_log_state("agent_node_creator - return", _return)
    return _return
