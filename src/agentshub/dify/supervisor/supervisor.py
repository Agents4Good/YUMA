from schema import AgentState, DifyState
from langgraph.types import Command


# Tool responsável por delegar a criação dos nodes e egdes do sistema
def supervisor_agent(
    state: AgentState,
) -> Command:
    
    yaml_metadata = create_yaml_and_metadata("Sistema do usuario", " ")
    novoState = DifyState(
        architecture_output= state["architecture_output"],
        metadata_dict= yaml_metadata
    )
    return Command(update=novoState, goto=["node_creator"])
