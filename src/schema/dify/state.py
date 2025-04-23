from langgraph.graph import MessagesState
from pydantic import Field
from typing import Dict, Annotated
import operator


class DifyState(MessagesState):
    architecture_output: Dict = Field(default=None, description="Stores the architecture output JSON.")
    metadata_dict: Dict = Field(default=None, description="Stores the metadata of Dify YAML in a Dictionary format.")
    nodes_dicts: Annotated[list, operator.add] = Field(default_factory=list, description="Stores the nodes of Dify YAML in a List of Dictionaries.")
    edges_dicts: Annotated[list, operator.add] = Field(default_factory=list, description="Stores the edges of Dify YAML in a List of Dictionaries.")
