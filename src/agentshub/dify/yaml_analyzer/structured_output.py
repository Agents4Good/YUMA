from pydantic import BaseModel, Field
from typing import List


class YamlAnalyzerOutput(BaseModel):
    """
    Represents the missing components.
    """
    message: str = Field(description="Explanation of the missing components")
    """
    Represents the Dify's agents that will build the missing components 
    """
    agents: List[str] = Field(description="List of Dify's agents that will build the missing components")
