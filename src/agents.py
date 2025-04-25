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
    create_http_node,
    write_dify_yaml,
    
)
from outputs import ArchitectureOutput, SupervisorOutput

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


structured_model = ChatOpenAI(
                        model=os.getenv("MODEL_ID"),
                        base_url=os.getenv("BASE_URL_DEEP_INFRA"),
                        model_kwargs={"response_format": {"type": "json_object"}})

start_node_creator_model = model.bind_tools(
    [create_start_node]
)

llm_node_creator_model = model.bind_tools(
    [create_llm_node]
)

answer_node_creator_model = model.bind_tools(
    [create_answer_node]
)

logic_node_creator_model = model.bind_tools(
    [create_contains_logic_node]
)

http_node_creator_model = model.bind_tools(
    [create_http_node]
)

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
        # create_not_empty_logic_node,
        create_http_node
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
        
        print("============================================================")
        print(last_ai_message)
        print("============================================================")
        
        var = model.invoke(f"A seguinte mensagem descreve um sistema que deve ser desenvolvido. Seu objetivo é informar o objetivo do sistema, extrair os requisitos do usuário e listar as funcionalidades principais. Descrição: {last_ai_message.content}")
        
        buffer = [SystemMessage(content=system_prompt).content] + [var.content] 

    print("============================================================")
    print(buffer)
    print("============================================================")

    response = structured_model.invoke(buffer)
    
    print("============================================================")
    print(response)
    print("============================================================")
    
    response = _extract_json(response.content, ArchitectureOutput)
    

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


def _extract_json(content, response_format):
    parser = JsonOutputParser(pydantic_object=response_format)
    response = None

    try:
        if isinstance(content, str) and "```" in content:
            print("================ Resposta é uma string com JSON ================")
            pattern = r"```(?:json)?\s*({.*?})\s*```"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                raw_json_str = match.group(1)
                parsed = parser.parse(raw_json_str)
                response = response_format(**parsed)

        elif isinstance(content, str):
            print("================ Resposta é uma string ================")
            json_start = content.find('{')
            if json_start != -1:
                raw_json_str = content[json_start:]
                parsed = json.loads(raw_json_str)
                response = response_format(**parsed)

        else:
            print("================ Resposta não é uma string ou JSON válido ================")
            print(content)
            
        return response

    except Exception as e:
        print("Erro ao parsear JSON:", e)
        print("Resposta bruta:", content)


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

# from langchain_core.prompts import FewShotPromptTemplate

# examples = [
#     {
#         "input": """
#         """
#     },
#     {
#     }
# ]

# prompt = FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=example_prompt,
#     suffix="Question: {input}",
#     input_variables=["input"],
# )

# Tool responsável por delegar a criação dos nodes e egdes do sistema
def supervisor_agent(
    state: AgentState,
) -> Command:
    system_prompt = agents_prompts.SUPERVISOR_AGENT

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
    print(response)
    
    response = _extract_json(response, SupervisorOutput)
    
    print("supervisor_agent executado")
    print(response)
    response.agents = response.agents.insert(0, 'start_node_creator')
    response.agents = response.agents.append('answer_node_creator')
    
    yaml_metadata = create_yaml_and_metadata("Sistema do usuario", " ")
    
    novoState = DifyState(
        messages= state["messages"] + AIMessage(response),
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

def llm_node_creator(state: DifyState) -> Command:
    system_prompt = agents_prompts.LLM_NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
   
    print("llm_node_creator executado")
    print(response)
    return Command(
        update={"messages": [response]}
    )

def start_node_creator(state: DifyState) -> Command:
    system_prompt = agents_prompts.START_NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
   
    print("start_node_creator executado")
    print(response)
    return Command(
        update={"messages": [response]}
    )
    
def answer_node_creator(state: DifyState) -> Command:
    system_prompt = agents_prompts.ANSWER_NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
   
    print("answer_node_creator executado")
    print(response)
    return Command(
        update={"messages": [response]}
    )
    
def logic_node_creator(state: DifyState) -> Command:
    system_prompt = agents_prompts.LOGIC_NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
   
    print("logic_node_creator executado")
    print(response)
    return Command(
        update={"messages": [response]}
    )
 
def http_node_creator(state: DifyState) -> Command:
    system_prompt = agents_prompts.HTTP_NODE_CREATOR

    messages = state["messages"] + [system_prompt]
    response = node_creator_dify_model.invoke(messages)
   
    print("http_node_creator executado")
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
    "create_logic_edges": create_logic_edges,
    "create_http_node": create_http_node
}

def call_dify_tools(state: DifyState) -> List[Command]:
    tool_calls = state["messages"][-1].tool_calls
    print(tool_calls)
    commands = []
    for tool_call in tool_calls:
        commands.append(tools_dify[tool_call["name"]].invoke(tool_call))

    return commands