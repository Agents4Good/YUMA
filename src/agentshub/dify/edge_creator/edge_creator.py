from schema.dify import DifyState
from langgraph.types import Command
from .prompt import EDGE_CREATOR
from models import model_dify
from agentshub import only_tools_agent
from langchain_core.messages import SystemMessage, HumanMessage
from utils.yuma import write_log_state
from .tools import create_edges, create_logic_edges


edge_creator_dify_model = model_dify.bind_tools(
    [
        create_edges,
        create_logic_edges
    ]
)

def _human_message(node_dicts:str, architecture: str):
    return HumanMessage(content=f"Aqui está a arquitetura do sistema:\n{architecture}"
                        + f"\n e os nodes criados:\n{node_dicts}")

# Agente responsável por criar as edges do sistema
def edge_creator(state: DifyState) -> Command:
    instruction = state.get("human_message", _human_message(state["nodes_dicts"], state["architecture_output"]))

    message = [SystemMessage(content=EDGE_CREATOR), instruction]
    _return = only_tools_agent(edge_creator_dify_model, message)
    write_log_state("edge_creator - return", _return)
    return _return
