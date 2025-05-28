from schema.dify import DifyState
from langgraph.types import Command
from langchain_core.messages import SystemMessage, BaseMessage
from schema.dify import DifyState
from langchain_core.language_models.chat_models import BaseChatModel
from utils import content_to_tool
from typing import List


def only_tools_agent(model: BaseChatModel, new_messages: List[BaseMessage], state: DifyState, max_retries: int = 3) -> Command:
    messages = state["messages"] + new_messages
    for _ in range(max_retries):
        response = model.invoke(messages)
        if response.content:
            response = content_to_tool(response)
        if getattr(response, "tool_calls", None):
            return Command(
                update={"messages": [response]}
            )
    
    raise RuntimeError(f"Nenhuma tool_call foi retornada após {max_retries} tentativas.")