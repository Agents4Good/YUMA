from schema.yuma import AgentState
from .prompt import SUPERVISOR_AGENT
from langgraph.types import Command
from langchain_core.messages import SystemMessage, AIMessage
from utils import extract_json
from models import structured_model
from .structured_output import SupervisorOutput
from schema.dify import DifyState
from tools.dify import create_yaml_metadata
from utils.yuma import write_log, write_log_state

# Tool responsável por delegar a criação dos nodes e egdes do sistema


def supervisor(
    state: AgentState,
) -> Command:
    system_prompt = SUPERVISOR_AGENT

    messages = state["messages"] + [SystemMessage(system_prompt)]
    response = structured_model.invoke(messages)

    response = extract_json(response.content, SupervisorOutput)

    write_log("supervisor_agent response", response)
    response.agents.insert(0, "start_node_creator")
    response.agents.append("answer_node_creator")

    yaml_metadata = create_yaml_metadata("Sistema do usuario", " ")

    supervisor_message = ", ".join(response.agents)
    novoState = DifyState(
        messages=state["messages"] + [AIMessage(supervisor_message)],
        architecture_output=state["architecture_output"],
        metadata_dict=yaml_metadata,
    )

    _return = Command(update=novoState)
    write_log_state("supervisor - return", _return)
    return _return
