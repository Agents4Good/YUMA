from schema.yuma import AgentState
from langgraph.types import Command, interrupt
from langchain_core.messages import HumanMessage
from utils.yuma import write_log_state


def human_node(
    state: AgentState,
) -> Command:
    """A node for collecting user input."""
    user_input = interrupt("Avalie a resposta do agente: ")
    active_agent = state["active_agent"]

    message = HumanMessage(content=user_input)
    
    key_phrase = "prossiga para a geração"
        
    goto = active_agent
    if active_agent == "architecture_agent" and message and key_phrase in message.content.lower():
        goto = "dify"

    _return = Command(
        update={
            "active_agent": active_agent,
            "human_inputs": state["human_inputs"] + [message],
        },
        goto=goto,
    )
    write_log_state("human_node - return", _return)
    return _return
