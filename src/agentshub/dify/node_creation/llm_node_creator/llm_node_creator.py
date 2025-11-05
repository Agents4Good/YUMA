from schema.dify import DifyState
from .prompt import LLM_NODE_CREATOR
from langgraph.types import Command
from agentshub import only_tools_agent
from utils.dify import build_few_shot
from .examples import EXAMPLES
from utils.yuma import write_log_state
from ..human_message import _human_message
from models import model_dify
from .tools import create_llm_node


llm_node_creator_model = model_dify.bind_tools(
    [create_llm_node]
)

def llm_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    human_message = state.get(
        "human_message", _human_message("LLM", archictecure))
    new_messages = build_few_shot(LLM_NODE_CREATOR, EXAMPLES, human_message)
    
    _return = only_tools_agent(llm_node_creator_model, state["messages"] + new_messages)
    write_log_state("llm_node_creator - return", _return)
    return _return
