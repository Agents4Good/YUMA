from schema.dify import DifyState
from .prompt import AGENT_NODE_CREATOR
from langgraph.types import Command
from models.dify import agent_node_creator_model
from schema.dify import DifyState
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot


def agent_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    new_messages = build_few_shot(
        archictecure, AGENT_NODE_CREATOR, EXAMPLES, "AGENTE")
    return only_tools_agent(agent_node_creator_model, new_messages, state)
