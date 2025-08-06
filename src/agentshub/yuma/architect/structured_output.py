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
    target: str = Field(
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

class Tool(BaseModel):
    """
    Represents a tool that an agent can use.
    """
    tool_name: str = Field(description="")
    description: str = Field(description="")


class AgentArchitectureOutput(BaseModel):
    """
    Represents the architecture of an AI agent, including its persona definition,
    task assignment, available tools, and flow control within the agent graph.
    """

    agent: str = Field(
        description=(
            "Name of the agent. This is a unique identifier used to reference this specific agent node in the system's graph."
        )
    )

    agent_role: str = Field(
        description=(
            "Description of the role (persona) assumed by the agent during its execution. "
            "It should include behavioral guidelines, expected objectives, and examples of how the agent should respond. "
            "This description is used as the system prompt to guide the agent's behavior.\n\n"
            "Example: 'You are a legal assistant responsible for summarizing court cases in plain language. "
            "Given a legal text, extract the parties involved, the main events, and the outcome, if present.'"
        )
    )

    agent_task: str = Field(
        description=(
            "The task that the agent is responsible for accomplishing. This is often derived from the user's objective "
            "and should be clearly defined to ensure the agent performs a focused and effective action."
        )
    )

    agent_type: str = Field(
        description=(
            "Specifies the type of agent. It determines whether the agent behaves as a conversational agent "
            "(interacting directly with the user) or as a tool agent (performing background operations)."
            "if is a conversational agent set it to CONVERSATIONAL"
            "if is a tool agent set it to TOOL"
        )
    )

    tools: List[Tool] = Field(
        description=(
            "A list of tools or APIs available to this agent. These tools define the set of actions the agent can take "
            "to complete its assigned task. Each tool includes a name, parameters, and expected outputs."
        )
    )

    flow: str = Field(
        description=(
            "The defined flow of interaction or execution for this agent within the larger graph of agents. "
            "This flow may describe which agent comes before or after in the logical sequence."
        )
    )

    route_next: bool = Field(
        default_factory=lambda: False,
        description=(
            "Determines whether the graph should proceed to the next agent node (`True`) or remain on the current node (`False`). "
            "Useful in scenarios where decision-making or conditional branching is required based on the agent's outcome."
        )
    )



