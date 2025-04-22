from schema import DifyState
from langgraph.types import Command
from prompt import EDGE_CREATOR
from models import edge_creator_dify_model


# Agente responsável por criar as edges do sistema
def edge_creator(state: DifyState) -> Command:
    print("edge_creator")
    system_prompt = EDGE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = edge_creator_dify_model.invoke(messages)
    print(response)
    # tool call para adicionar os arcos no YAML
    print("edge_creator executado")
    return Command(
        update={"messages": [response]},
    )
