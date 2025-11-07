from schema.yuma import AgentState
from .prompt import ARCHITECT_AGENT 
from langgraph.types import Command
from typing import Literal
from langchain_core.messages import SystemMessage, AIMessage
from models import model_sys
from .structured_output import ArchitectureOutput
from tools.yuma.utils import sequence_diagram_generator
from utils.yuma import write_log_state, write_log


structured_model = model_sys.with_structured_output(ArchitectureOutput)

# Agente responsável por criar a arquitetura do sistema com base nos requisitos
def architect(state: AgentState,
            max_retries: int = 3
            ) -> Command[Literal["human_node", "dify"]]:
    system_prompt = ARCHITECT_AGENT
    for _ in range(max_retries):
        try:
            messages = state.get(
                "messages") + [SystemMessage(content=system_prompt)] + state.get("human_inputs")
            response = structured_model.invoke(messages)
            if response is None:
                continue

            goto = "human_node"
            if response.route_next:
                goto = "dify"
                state["messages"].append(AIMessage(content=response.model_dump_json()))

            sequence_diagram_generator.invoke(response.model_dump_json())

            _return = Command(
                update={
                    "messages": state["messages"],
                    "active_agent": "architecture_agent",
                    "agente_name": "Arquiteto do Sistema",
                    "architecture_output": response,
                },
                goto=goto,
            )
            write_log_state("architect - return", _return)
            return _return
        
        except Exception as e:
            write_log(f'architect - Falha após várias tentativas', e)
            return Command(update=state, goto="human_node")
