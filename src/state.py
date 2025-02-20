from typing_extensions import Annotated
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """
    This field should be used to store the active agent in the graph.
    """
    active_agent: Annotated[str, "UML codes with theirs diagram type"]