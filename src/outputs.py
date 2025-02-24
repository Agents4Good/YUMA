from pydantic import BaseModel, Field
from typing import Dict, List

class Agent(BaseModel):
    """
    This class should be used to describe the agent that will be generated.
    """
    agent: str = Field(description="The name of the agent")
    prompt: str = Field(description="The description of the agent")

class ArchitectureOutput(BaseModel):
    """
    This output should be used to store the architecture of the multiagent system that will be generated.
    """
    agents: List[Agent] = Field(description="The agents of the multiagent system")
    interactions: Dict[Agent, List[Agent]] = Field(description="The interactions between the agents, "
                                                            "where the key is an agent and the value is a list of agents it interacts with.")
