from schema.dify import DifyState
from .prompt import LOGIC_NODE_CREATOR
from langgraph.types import Command
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot
from utils.yuma import write_log_state
from ..human_message import _human_message
from models import model_dify
from .tools import (create_contains_logic_node, 
                    create_not_contains_logic_node, 
                    create_start_with_logic_node, 
                    create_end_with_logic_node, 
                    create_is_equals_logic_node,
                    create_not_empty_logic_node,
                    create_not_equals_logic_node,
                    create_is_empty_logic_node)


logic_node_creator_model = model_dify.bind_tools(
    [create_contains_logic_node,
     create_not_contains_logic_node,
     create_start_with_logic_node,
     create_end_with_logic_node,
     create_is_equals_logic_node,
     create_not_equals_logic_node,
     create_is_empty_logic_node,
     create_not_empty_logic_node,
     ]
)

def logic_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    human_message = state.get(
        "human_message", _human_message("LÓGICA", archictecure))
    new_messages = build_few_shot(LOGIC_NODE_CREATOR, EXAMPLES, human_message)
    
    _return = only_tools_agent(logic_node_creator_model, state["messages"] + new_messages)
    write_log_state("logic_node_creator - return", _return)
    return _return
