from langgraph.types import Command
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from utils import content_to_tool
from typing import List


def only_tools_agent(model: BaseChatModel, new_messages: List[BaseMessage], max_retries: int = 3) -> Command:
    for _ in range(max_retries):
        response = model.invoke(new_messages)
        if response.content:
            response = content_to_tool(response)
        if getattr(response, "tool_calls", None):
            return Command(
                update={"messages": [response]}
            )
    
    raise RuntimeError(f"Nenhuma tool_call foi retornada após {max_retries} tentativas.")