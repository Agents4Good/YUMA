from langgraph.graph import MessagesState
from pydantic import Field
from typing import List, Dict, Optional
from langchain_core.messages.base import BaseMessage


class AgentState(MessagesState):
    active_agent: str = Field(
        description="This field should be used to store the active agent in the graph."
    )
    architecture_output: Optional[Dict] = Field(
        default=None, description="Stores the architecture output JSON."
    )
    buffer: List[BaseMessage] = Field(description="the messages of the active agent.")
