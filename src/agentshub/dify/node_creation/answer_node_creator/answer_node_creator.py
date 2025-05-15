from schema.dify import DifyState
from .prompt import ANSWER_NODE_CREATOR
from langgraph.types import Command
from models.dify import answer_node_creator_model
from schema.dify import DifyState
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot


def answer_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(
        archictecure, ANSWER_NODE_CREATOR, EXAMPLES, "ANSWER")
    return only_tools_agent(answer_node_creator_model, new_messages, state)
