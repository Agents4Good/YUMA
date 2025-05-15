from schema.dify import DifyState
from .prompt import LLM_NODE_CREATOR
from langgraph.types import Command
from models.dify import llm_node_creator_model
from agentshub import only_tools_agent
from utils.dify import build_few_shot
from .examples import EXAMPLES


def llm_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(
        archictecure, LLM_NODE_CREATOR, EXAMPLES, "LLM")
    return only_tools_agent(llm_node_creator_model, new_messages, state)
