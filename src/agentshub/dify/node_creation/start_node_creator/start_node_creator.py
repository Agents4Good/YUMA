from schema.dify import DifyState
from .prompt import START_NODE_CREATOR
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from models.dify import start_node_creator_model
from schema.dify import DifyState


def start_node_creator(state: DifyState) -> Command:
    system_prompt = START_NODE_CREATOR

    messages = state["messages"] + [SystemMessage(system_prompt)]
    response = start_node_creator_model.invoke(messages)

    print("start_node_creator executado\n", response)
    return Command(
        update={"messages": [response]}
    )
