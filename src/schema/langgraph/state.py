from langgraph.graph import MessagesState
from pydantic import Field
from typing import List, Dict, Optional
from langchain_core.messages.base import BaseMessage


class LangState(MessagesState):
    active_agent: str = Field(
        description="This field should be used to store the active agent in the graph."
    )
    architecture_output: Optional[Dict] = Field(
        default=None, description="Stores the architecture output JSON."
    )