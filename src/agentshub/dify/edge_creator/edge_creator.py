from schema.dify import DifyState
from langgraph.types import Command
from .prompt import EDGE_CREATOR
from models.dify import edge_creator_dify_model
from utils.genia import write_log_state


# Agente responsável por criar as edges do sistema
def edge_creator(state: DifyState) -> Command:
    system_prompt = EDGE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = edge_creator_dify_model.invoke(messages)
    # tool call para adicionar os arcos no YAML
    _return = Command(
        update={"messages": [response]},
    )
    write_log_state("edge_creator - return", _return)
    return _return
