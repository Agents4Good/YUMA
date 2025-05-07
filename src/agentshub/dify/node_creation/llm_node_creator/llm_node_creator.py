from schema.dify import DifyState
from .prompt import LLM_NODE_CREATOR
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from models.dify import llm_node_creator_model
from schema.dify import DifyState


def llm_node_creator(state: DifyState) -> Command:
    system_prompt = LLM_NODE_CREATOR

    messages = state["messages"] + [SystemMessage(system_prompt)]
    response = llm_node_creator_model.invoke(messages)

    print("llm_node_creator executado")
    return Command(
        update={"messages": [response]}
    )
