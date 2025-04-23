# from pydantic import BaseModel, Field
# from typing import List, Dict

# class Agent(BaseModel):
#     """
#     Represents an agent in the multi-agent system.
#     """
#     agent: str = Field(description="The name of the agent using underlines")
#     description: str = Field(description="The description of the agent")

# class Interaction(BaseModel):
#     """
#     Represents an interaction between agents.
#     """
#     source: str = Field(description="The name of the source agent using underlines")
#     targets: str = Field(description="The target agent that the source agent interacts with, using underlines")
#     description: str = Field(description="A short description of what a agent will comunicate the other")

# class ArchitectureOutput(BaseModel):
#     """
#     Represents the architecture of the multi-agent system.
#     """
#     agents: List[Agent] = Field(description="List of agents in the multi-agent system")
#     interactions: List[Interaction] = Field(description="List of interactions between agents, "
#                                                         "where each interaction has a source agent and a target agent")
#     route_next: bool = Field(default_factory=lambda: False, description="Determines if the graph should proceed to the next node (True) or remain in the current node (False).")