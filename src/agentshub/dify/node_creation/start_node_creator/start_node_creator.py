from schema.dify import DifyState
from .prompt import START_NODE_CREATOR
from langgraph.types import Command
from models.dify import start_node_creator_model
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot


def start_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(
        archictecure, START_NODE_CREATOR, EXAMPLES, "START")
    return only_tools_agent(start_node_creator_model, new_messages, state)
