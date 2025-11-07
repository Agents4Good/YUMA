from typing import Annotated
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from utils.yuma.plantuml_parser import generate_diagram, json_to_plantuml


@tool("sequence_diagram_generator")
def sequence_diagram_generator(architecture_output: str):
    """
    Converte a saída do agente de arquitetura em um diagrama de sequência PlantUML e gera uma imagem do diagrama.
    Retorna o caminho do arquivo gerado.
    """
    plantuml_output = json_to_plantuml(architecture_output)
    generate_diagram(plantuml_output)


@tool("engineer_to_architect")
def handoff_to_agent(
    fianl_documentation: str,
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    """Ask another agent for help."""
    tool_message = {
        "role": "tool",
        "content": f"Successfully transferred to architect",
        "name": "engineer_to_architect",
        "tool_call_id": tool_call_id,
    }
    
    return Command(
        # navigate to another agent node in the PARENT graph
        #goto=agent_name,
        #graph=Command.PARENT,
        # This is the state update that the agent `agent_name` will see when it is invoked.
        # We're passing agent's FULL internal message history AND adding a tool message to make sure
        # the resulting chat history is valid.
        update={"messages": state["messages"] + [tool_message],
                "human_inputs": [],
                "specification": fianl_documentation,
                },
        goto="architecture_agent"
    )