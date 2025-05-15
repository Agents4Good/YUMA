from schema.dify import DifyState
from .prompt import LOGIC_NODE_CREATOR
from langgraph.types import Command
from models.dify import logic_node_creator_model
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot


def logic_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(
        archictecure, LOGIC_NODE_CREATOR, EXAMPLES, "LÓGICA")
    return only_tools_agent(logic_node_creator_model, new_messages, state)
