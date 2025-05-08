from schema.dify import DifyState
from .prompt import AGENT_NODE_CREATOR
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from models.dify import agent_node_creator_model
from schema.dify import DifyState


def agent_node_creator(state: DifyState) -> Command:
    system_prompt = AGENT_NODE_CREATOR

    messages = state["messages"] + [SystemMessage(system_prompt)]
    response = agent_node_creator_model.invoke(messages)

    print("agent_node_creator executado")
    return Command(
        update={"messages": [response]}
    )
