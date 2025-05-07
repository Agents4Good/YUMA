from schema.dify import DifyState
from .prompt import LOGIC_NODE_CREATOR
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from models.dify import logic_node_creator_model
from schema.dify import DifyState


def logic_node_creator(state: DifyState) -> Command:
    system_prompt = LOGIC_NODE_CREATOR

    messages = state["messages"] + [SystemMessage(system_prompt)]
    response = logic_node_creator_model.invoke(messages)

    print("logic_node_creator executado\n", response)
    return Command(
        update={"messages": [response]}
    )
