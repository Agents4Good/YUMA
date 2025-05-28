from schema.yuma import AgentState
from langgraph.types import Command, interrupt
from langchain_core.messages import HumanMessage
from typing import Literal
from utils.yuma import write_log_state


def human_node(
    state: AgentState,
) -> Command[Literal["requirements_engineer", "architecture_agent"]]:
    """A node for collecting user input."""
    user_input = interrupt("Avalie a resposta do agente: ")
    active_agent = state["active_agent"]

    message = HumanMessage(content=user_input)

    buffer = state.get("buffer", [])
    if buffer:
        buffer.append(message)

    _return = Command(
        update={
            "messages": state["messages"] + [message],
            "buffer": buffer,
            "active_agent": active_agent,
            "architecture_output": state.get("architecture_output", None),
        },
        goto=active_agent,
    )
    write_log_state("human_node - return", _return)
    return _return
