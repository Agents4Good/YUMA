from schema.dify import DifyState
from .prompt import ANSWER_NODE_CREATOR
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from models.dify import answer_node_creator_model
from schema.dify import DifyState


def answer_node_creator(state: DifyState) -> Command:
    system_prompt = ANSWER_NODE_CREATOR

    messages = state["messages"] + [SystemMessage(system_prompt)]
    print("answer_node_creator executado")
    response = answer_node_creator_model.invoke(messages)
   
    print(response)
    return Command(
        update={"messages": [response]}
    )
    