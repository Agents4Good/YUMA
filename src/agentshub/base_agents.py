from schema.dify import DifyState
from langgraph.types import Command
from langchain_core.messages import SystemMessage, BaseMessage
from schema.dify import DifyState
from langchain_core.language_models.chat_models import BaseChatModel
from utils import content_to_tool
from typing import List


def only_tools_agent(model: BaseChatModel, new_messages: List[BaseMessage], state: DifyState) -> Command:
    messages = state["messages"] + new_messages
    response = model.invoke(messages)

    if response.content:
        response = content_to_tool(response)

    return Command(
        update={"messages": [response]}
    )
