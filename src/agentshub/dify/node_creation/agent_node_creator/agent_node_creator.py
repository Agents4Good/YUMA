from schema.dify import DifyState
from .prompt import AGENT_NODE_CREATOR
from langgraph.types import Command
from schema.dify import DifyState
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot
from utils.yuma import write_log_state
from ..human_message import _human_message
from models import model_dify
from .tools import create_agent_node


agent_node_creator_model = model_dify.bind_tools(
    [
        create_agent_node
    ]
)

def agent_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    human_message = state.get(
        "human_message", _human_message("AGENTE", archictecure))
    
    new_messages = build_few_shot(AGENT_NODE_CREATOR, EXAMPLES, human_message)
    
    _return = only_tools_agent(agent_node_creator_model, state["messages"] + new_messages)
    write_log_state("agent_node_creator - return", _return)
    return _return
