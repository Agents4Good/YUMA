from schema.dify import DifyState
from .prompt import ANSWER_NODE_CREATOR
from langgraph.types import Command
from models.dify import answer_node_creator_model
from schema.dify import DifyState
from agentshub import only_tools_agent
from utils.genia import write_log_state


def answer_node_creator(state: DifyState) -> Command:
    _return = only_tools_agent(answer_node_creator_model, ANSWER_NODE_CREATOR, state)
    write_log_state("answer_node_creator - return", _return)
    return _return
