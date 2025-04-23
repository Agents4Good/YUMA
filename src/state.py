# from langgraph.graph import MessagesState
# from pydantic import BaseModel, Field
# from typing import List, Dict, Optional, Annotated
# from langchain_core.messages.base import BaseMessage
# import operator

# class AgentState(MessagesState):
#     active_agent: str = Field(description="This field should be used to store the active agent in the graph.")
#     architecture_output: Optional[Dict] = Field(default=None, description="Stores the architecture output JSON.")
#     buffer: List[BaseMessage]= Field(description="the messages of the active agent.")

# class DifyState(MessagesState):
#     architecture_output: Dict = Field(default=None, description="Stores the architecture output JSON.")
#     metadata_dict: Dict = Field(default=None, description="Stores the metadata of Dify YAML in a Dictionary format.")
#     nodes_dicts: Annotated[list, operator.add] = Field(default_factory=list, description="Stores the nodes of Dify YAML in a List of Dictionaries.")
#     edges_dicts: Annotated[list, operator.add] = Field(default_factory=list, description="Stores the edges of Dify YAML in a List of Dictionaries.")