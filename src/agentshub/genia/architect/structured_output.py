from pydantic import BaseModel, Field
from typing import List


class Node(BaseModel):
    """
    Represents an node in the multi-agent system.
    """

    node: str = Field(description="The name of the node using underlines")
    description: str = Field(description="The description of the node")


class Interaction(BaseModel):
    """
    Represents an interaction between nodes.
    """

    source: str = Field(description="The name of the source node using underlines")
    targets: str = Field(
        description="The target node that the source node interacts with, using underlines"
    )
    description: str = Field(
        description="A short description of what a node will comunicate the other"
    )


class ArchitectureOutput(BaseModel):
    """
    Represents the architecture of the multi-agent system.
    """

    nodes: List[Node] = Field(description="List of nodes in the multi-agent system")
    interactions: List[Interaction] = Field(
        description="List of interactions between nodes, "
        "where each interaction has a source node and a target node"
    )
    route_next: bool = Field(
        default_factory=lambda: False,
        description="Determines if the graph should proceed to the next node (True) or remain in the current node (False).",
    )
