from state import AgentState, DifyState
from tools import (
    make_handoff_tool,
    sequence_diagram_generator,
    create_yaml_and_metadata,
    create_llm_node,
    create_edges,
    create_logic_edges,
    create_answer_node,
    create_start_node,
    create_start_with_logic_node,
    create_end_with_logic_node,
    create_contains_logic_node,
    create_not_contains_logic_node,
    create_is_equals_logic_node,
    create_not_equals_logic_node,
    create_is_empty_logic_node,
    create_not_empty_logic_node,
    write_dify_yaml,
    
)
from outputs import ArchitectureOutput

from langgraph.prebuilt import create_react_agent
from langgraph.types import Command, interrupt
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from prompts import agents_prompts
from typing import Literal, List
from dotenv import load_dotenv
from utils.dify_gateway import dify_import_yaml
import os
from langchain_core.output_parsers import JsonOutputParser
import re
import json


load_dotenv(override=True)

architecture_tool = [make_handoff_tool(agent_name="architecture_agent")]
end_tool = [make_handoff_tool(agent_name="__end__")]

model = ChatOpenAI(model=os.getenv("MODEL_ID"), base_url=os.getenv("BASE_URL_DEEP_INFRA"))

architecture_model = model

node_creator_dify_model = model.bind_tools(
    [
        create_start_node,
        create_llm_node,
        create_answer_node,
        # create_start_with_logic_node,
        # create_end_with_logic_node,
        create_contains_logic_node,
        # create_not_contains_logic_node,
        # create_is_equals_logic_node,
        # create_not_equals_logic_node,
        # create_is_empty_logic_node,
        # create_not_empty_logic_node
     ]
)
edge_creator_dify_model = model.bind_tools([create_edges, create_logic_edges])


# Agente reponsável por analisar os requisitos do sistema e conversar com o usuário
def requirements_engineer(
    state: AgentState,
) -> Command[Literal["human_node", "architecture_agent"]]:
    system_prompt = agents_prompts.REQUIREMENTS_ENGINEER
    requirements_engineer_model = create_react_agent(
        model, tools=architecture_tool, prompt=system_prompt
    )
    response = requirements_engineer_model.invoke(state)
    response["active_agent"] = "requirements_engineer"
    return Command(update=response, goto="human_node")


# Agente responsável por criar a arquitetura do sistema com base nos requisitos
def architecture_agent(state: AgentState) -> Command[Literal["human_node", "dify"]]:
    system_prompt = agents_prompts.ARCHITECTURE_AGENT
    buffer = state.get("buffer", [])
    if not buffer:
        filtered_messages = [
            msg
            for msg in state["messages"]
            if isinstance(msg, AIMessage) and msg.content.strip() != ""
        ]

        last_ai_message = next(
            (msg for msg in reversed(filtered_messages) if isinstance(msg, AIMessage)),
            None,
        )

        buffer = [last_ai_message] + [SystemMessage(content=system_prompt)]
    
    parser = JsonOutputParser(pydantic_object=ArchitectureOutput)

    response = architecture_model.invoke(buffer)
    content = response.content
    try:
        if "```" in content:
            pattern = r'```(?:json)?\s*(.*?)```'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                raw_json_str = match.group(1)
                response = parser.parse(raw_json_str)
                response = ArchitectureOutput(**response)
        elif isinstance(content, dict) :
            parsed = json.loads(content)
            response = ArchitectureOutput(**parsed)
        if isinstance(content, str):
            parsed = json.loads(content)
            response = ArchitectureOutput(**parsed)
        if isinstance(content, ArchitectureOutput):
            response = ArchitectureOutput(**content)
    except Exception as e:
        print("Erro ao parsear JSON:", e)
        print("Resposta bruta:", content)
    
    print("response")
    print(response)
        
    goto = "human_node"
    if response.route_next:
        goto = "dify"

    sequence_diagram_generator.invoke(response.model_dump_json())

    buffer.append(AIMessage(content=response.model_dump_json()))

    return Command(
        update={
            "messages": state["messages"],
            "active_agent": "architecture_agent",
            "architecture_output": response,
            "buffer": buffer,
        },
        goto=goto,
    )


# Nó que representa a interação do usuário com o sistema
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

    return Command(
        update={
            "messages": state["messages"] + [message],
            "buffer": buffer,
            "active_agent": active_agent,
            "architecture_output": state.get("architecture_output", None),
        },
        goto=active_agent,
    )


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


# Agente responsável por criar os nodes do sistema
def node_creator(state: DifyState) -> Command:
    system_prompt = agents_prompts.NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
    print(response)
    # tool call para adicionar os nós no YAML
    print("node_creator executado")
    print(response)
    return Command(
        update={"messages": [response]}
    )


# Agente responsável por criar as edges do sistema
def edge_creator(state: DifyState) -> Command:
    print("edge_creator")
    system_prompt = agents_prompts.EDGE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = edge_creator_dify_model.invoke(messages)
    print(response)
    # tool call para adicionar os arcos no YAML
    print("edge_creator executado")
    return Command(
        update={"messages": [response]},
    )


def dify_yaml_builder(state: DifyState) -> Command:
    write_dify_yaml(state)
    try:
        dify_import_yaml("dify.yaml", "local")
    except Exception as e:
        print("Não foi possível importar o yaml para o app Dify local, tentando importar na web")
        try:
            dify_import_yaml("dify.yaml", "web")
        except Exception as e:
            print(e)
            print("Não foi possível importar o yaml para o app Dify local")

    return Command(
        update={"messages": [SystemMessage(content="Successfully create the dify yaml")]},
    )

tools_dify = {
    "create_llm_node" : create_llm_node,
    "create_answer_node" : create_answer_node,
    "create_start_node" : create_start_node,
    # "create_start_with_logic_node": create_start_with_logic_node,
    # "create_end_with_logic_node": create_end_with_logic_node,
    "create_contains_logic_node": create_contains_logic_node,
    # "create_not_contains_logic_node": create_not_contains_logic_node,
    # "create_is_equals_logic_node": create_is_equals_logic_node,
    # "create_not_equals_logic_node": create_not_equals_logic_node,
    # "create_is_empty_logic_node": create_is_empty_logic_node,
    # "create_not_empty_logic_node": create_not_empty_logic_node,
    "create_edges" : create_edges,
    "create_logic_edges": create_logic_edges
}

def call_dify_tools(state: DifyState) -> List[Command]:
    tool_calls = state["messages"][-1].tool_calls
    print(tool_calls)
    commands = []
    for tool_call in tool_calls:
        commands.append(tools_dify[tool_call["name"]].invoke(tool_call))

    return commands