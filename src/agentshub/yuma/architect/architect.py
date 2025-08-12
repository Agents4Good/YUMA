from schema.yuma import AgentState
from .prompt import ARCHITECT_AGENT, ARCHITECT_AGENT_DIFY, ARCHITECT_AGENT_SINGLE_REFINED
from langgraph.types import Command
from typing import Literal
from langchain_core.messages import SystemMessage, AIMessage
from models import structured_model
from utils import extract_json
from .structured_output import ArchitectureOutput, AgentArchitectureOutput
from tools.yuma.utils import sequence_diagram_generator
from utils.yuma import write_log_state, write_log

structured_model = structured_model.with_structured_output(AgentArchitectureOutput)

# Agente responsável por criar a arquitetura do sistema com base nos requisitos
def architect(state: AgentState,
            max_retries: int = 3
            ) -> Command[Literal["human_node", "code_generator"]]:
    system_prompt = ARCHITECT_AGENT_SINGLE_REFINED
    buffer = state.get("buffer", [])
    
    if not buffer:
        filtered_messages = [
            msg
            for msg in state["messages"]
            if isinstance(msg, AIMessage) and msg.content.strip() != ""
        ]

        ai_messages = [
            msg for msg in reversed(filtered_messages)
            if isinstance(msg, AIMessage)
        ]

        last_ai_message = ai_messages[1] if len(ai_messages) > 1 else None

        buffer = [SystemMessage(
            content=system_prompt).content] + [last_ai_message.content]

    for _ in range(max_retries):
        try:
            response = structured_model.invoke(buffer)
            #response = extract_json(response.content, ArchitectureOutput)

            #if response is None:
            #    continue

            goto = "human_node"
            if response.route_next:
                goto = "code_generator"
            
            state["messages"].append(AIMessage(content=response.model_dump_json()))
            
            #sequence_diagram_generator.invoke(response.model_dump_json())
            buffer.append(AIMessage(content=response.model_dump_json()))

            _return = Command(
                update={
                    "messages": state["messages"],
                    "active_agent": "architecture_agent",
                    "architecture_output": response,
                    "buffer": buffer,
                },
                goto=goto,
            )
            write_log_state("architect - return", _return)
            return _return
        
        except Exception as e:
            write_log(f'architect - Falha após várias tentativas', e)
            return Command(update=state, goto="human_node")
