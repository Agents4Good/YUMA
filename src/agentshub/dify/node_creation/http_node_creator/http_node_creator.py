from schema.dify import DifyState
from .prompt import HTTP_NODE_CREATOR
from langgraph.types import Command
from models.dify import http_node_creator_model
from agentshub import only_tools_agent
from langchain_core.messages import SystemMessage
from .examples import EXAMPLES
from utils.dify import build_few_shot


def http_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(
        archictecure, HTTP_NODE_CREATOR, EXAMPLES, "HTTP")
    return only_tools_agent(http_node_creator_model, new_messages, state)
