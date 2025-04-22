from schema import DifyState
from langgraph.types import Command
from prompt import NODE_CREATOR
from models import node_creator_dify_model


# Agente responsável por criar os nodes do sistema
def node_creator(state: DifyState) -> Command:
    system_prompt = NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
    print(response)
    # tool call para adicionar os nós no YAML
    print("node_creator executado")
    print(response)
    return Command(
        update={"messages": [response]}
    )
