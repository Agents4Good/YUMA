import yaml
import os

from utils.io_functions import get_path
from state import DifyState
from typing import Annotated, Literal

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from utils.plantuml_parser import generate_diagram, json_to_plantuml
from utils.tools_utils import create_logic_node, insert_node_yaml, insert_edge_yaml
import threading
from pathlib import Path

YAML_PATH = get_path("dify.yaml")
semaphore = threading.Semaphore(1)



def make_handoff_tool(*, agent_name: str):
    """Create a tool that can return handoff via a Command"""
    tool_name = f"transfer_to_{agent_name}"

    @tool(tool_name)
    def handoff_to_agent(
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Ask another agent for help."""
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": tool_name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            # navigate to another agent node in the PARENT graph
            goto=agent_name,
            graph=Command.PARENT,
            # This is the state update that the agent `agent_name` will see when it is invoked.
            # We're passing agent's FULL internal message history AND adding a tool message to make sure
            # the resulting chat history is valid.
            update={"messages": state["messages"] + [tool_message]},
        )

    return handoff_to_agent


@tool("sequence_diagram_generator")
def sequence_diagram_generator(architecture_output: str):
    """
    Converte a saída do agente de arquitetura em um diagrama de sequência PlantUML e gera uma imagem do diagrama.
    Retorna o caminho do arquivo gerado.
    """
    plantuml_output = json_to_plantuml(architecture_output)
    generate_diagram(plantuml_output)


def create_yaml_and_metadata(name: str, descritption: str):
    """
    Cria um arquivo YAML contendo os metadados do workflow.

    Parâmetros:
        - name (str): Nome do workflow.
        - description (str): Descrição do workflow.
    """
    return {
        "app": {"description": descritption, "mode": "advanced-chat", "name": name},
        "version": "0.1.5",
        "workflow": {
            "conversation_variables": [],
            "environment_variables": [],
            "graph": {"edges": [], "nodes": []},
        },
    }


@tool
def create_start_node(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    title: str, node_id: str
    ):
    """
    Cria o nó inicial do workflow responsável por capturar as entradas do usuário.

    Esta é a etapa inicial do workflow.

    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
    """
    start_node = {
        "id": node_id,
        "type": "custom",
        "data": {"desc": "", "title": title, "type": "start", "variables": []},
    }
    
    print("START NODE")
    return Command(
        update={
            "nodes_dicts" : [start_node],
            "messages": [
                ToolMessage(
                    "Successfully added the start node", tool_call_id=tool_call_id
                )]
        }
    )


@tool
def create_llm_node(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    title: str,
    node_id: str,
    role: str,
    context_variable: str,
    task: str,
    temperature: float,
):
    """
    Cria um nó de agente (LLM) para um workflow multiagente.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - role (str): Papel do agente no workflow (exemplo: "Você é um especialista em contar piadas").
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
        - task (str): O que o agente faz. Para receber os dados do nó anterior use exatamente "{{#context#}}". (exemplo: "Seu trabalho é responder a pergunta: "{{#context#}}").
        - temperature (float): Criatividade do modelo, entre 0 e 1.
    """
    llm_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "context": {
                "enabled": True,
                "variable_selector": [
                    context_variable.split(".")[0],
                    context_variable.split(".")[1],
                ]
                if context_variable
                else [],
            },
            "desc": "",
            "model": {
                "completion_params": {"temperature": temperature},
                "mode": "chat",
                "name": "claude-3-haiku-20240307",
                "provider": "langgenius/anthropic/anthropic",
            },
            "prompt_template": [{"role": "system", "text": f"""{role}\n{task}"""}],
            "title": title,
            "type": "llm",
            "variables": [],
            "vision": {"enabled": False},
        },
    }
    print("LLM NODE")
    return Command(
        update={
            "nodes_dicts" : [llm_node],
            "messages": [
                ToolMessage(
                    "Successfully added the LLM node", tool_call_id=tool_call_id
                )]
        }
    )


@tool
def create_answer_node(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    title: str, node_id: str, answer_variables: list[str]):
    """
    Cria o nó final do workflow responsável por exibir os outputs.

    Esse nó deve ser criado por último no workflow.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - answer_variables (list[str]): Lista de variáveis a serem exibidas para o usuário em ordem de disposição (exemplo: ["llm1.text", "llm2.text"]).
    """
    answer_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "answer": "".join(["{{#" + f"{variable}" + "#}}\n" for variable in answer_variables]).strip(),
            "desc": "",
            "title": title,
            "type": "answer",
            "variables": [],
        },
    }
    
    print("ANSWER NODE")
    return Command(
        update={
            "nodes_dicts" : [answer_node],
            "messages": [
                ToolMessage(
                    "Successfully added the answer node", tool_call_id=tool_call_id
                )]
        }
    )


@tool
def create_edges(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    edge_id: str,
    source_id: str,
    target_id: str
):
    """
    Cria uma aresta entre dois nós no workflow.
    
    Parâmetros:
        - edge_id (str): Identificador único da aresta (minúsculas, sem caracteres especiais).
        - source_id (str): ID do nó de origem da aresta (exemplo: "start_node", "llm1").
        - target_id (str): ID do nó de destino da aresta (exemplo: "answer_node", "llm2").
    """
    edge = {"id": edge_id, "source": source_id, "target": target_id, "type": "custom"}
    
    print("CREATE EDGE")
    return Command(
        update={
            "edges_dicts" : [edge],
            "messages": [
                ToolMessage(
                    f"Successfully added the edge between {source_id} and {target_id}", tool_call_id=tool_call_id
                )]
        }
    )
   

@tool
def create_logic_edges(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    edge_id: str,
    source_id: str,
    source_handle: Literal["true", "false"],
    target_id: str
):
    """
    Cria uma aresta entre um nó de lógica e outro nó qualquer do workflow.
    Há duas saídas do mesmo nó de lógica, uma para "true" e outra para "false".
    
    Parâmetros:
        - edge_id (str): Identificador único da aresta (minúsculas, sem caracteres especiais).
        - source_id (str): ID do nó de lógica (exemplo: "start_with_node").
        - source_handle (Literal["true", "false"]): Para qual saída booleana a aresta deve ser criada.
        - target_id (str): ID do nó de destino da aresta (exemplo: "llm1", "llm2").
    """
    logic_edge = {"id": edge_id, "source": source_id, "sourceHandle": source_handle, "target": target_id, "type": "custom"}
    
    print("CREATE LOGIC EDGE")
    return Command(
        update={
            "edges_dicts" : [logic_edge],
            "messages": [
                ToolMessage(
                    f"Successfully added logic edge between {source_id} and {target_id}", tool_call_id=tool_call_id
                )]
        }
    ) 


@tool
def create_start_with_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    value: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável começa com um valor específico.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - value (str): Valor a ser verificado se é o início da variável.
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    start_with_node = create_logic_node(
        title=title,
        node_id=node_id,
        value=value,
        comparison_operator="start with",
        context_variable=context_variable
    )
    
    print("START WITH NODE")
    return Command(
        update={
            "nodes_dicts" : [start_with_node],
            "messages": [
                ToolMessage(
                    "Successfully added start with node", tool_call_id=tool_call_id
                )]
        }
    )
    
    
@tool
def create_end_with_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    value: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável termina com um valor específico.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - value (str): Valor a ser verificado se é o final da variável.
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    end_with_node = create_logic_node(
        title=title,
        node_id=node_id,
        value=value,
        comparison_operator="end with",
        context_variable=context_variable
    )
    
    print("END WITH NODE")
    return Command(
        update={
            "nodes_dicts" : [end_with_node],
            "messages": [
                ToolMessage(
                    "Successfully added end with node", tool_call_id=tool_call_id
                )]
        }
    )
    
    
@tool
def create_contains_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    value: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável contém um valor específico.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - value (str): Valor a ser verificado se está contido na variável.
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    contains_node = create_logic_node(
        title=title,
        node_id=node_id,
        value=value,
        comparison_operator="contains",
        context_variable=context_variable
    )
    
    print("CONTAINS NODE")
    return Command(
        update={
            "nodes_dicts" : [contains_node],
            "messages": [
                ToolMessage(
                    "Successfully added contains node", tool_call_id=tool_call_id
                )]
        }
    )

    
@tool
def create_not_contains_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    value: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável não contém um valor específico.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - value (str): Valor a ser verificado se não está contido na variável.
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    not_contains_node = create_logic_node(
        title=title,
        node_id=node_id,
        value=value,
        comparison_operator="not contains",
        context_variable=context_variable
    )
    
    print("NOT CONTAINS NODE")
    return Command(
        update={
            "nodes_dicts" : [not_contains_node],
            "messages": [
                ToolMessage(
                    "Successfully added not contains node", tool_call_id=tool_call_id
                )]
        }
    )

    
@tool
def create_is_equals_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    value: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável é igual a um valor específico.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - value (str): Valor a ser verificado se é igual à variável.
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    is_equals_node = create_logic_node(
        title=title,
        node_id=node_id,
        value=value,
        comparison_operator="is",
        context_variable=context_variable
    )
    
    print("IS EQUALS NODE")
    return Command(
        update={
            "nodes_dicts" : [is_equals_node],
            "messages": [
                ToolMessage(
                    "Successfully added is equals node", tool_call_id=tool_call_id
                )]
        }
    )

    
@tool
def create_not_equals_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    value: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável não é igual a um valor específico.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - value (str): Valor a ser verificado se não é igual à variável.
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    not_equals_node = create_logic_node(
        title=title,
        node_id=node_id,
        value=value,
        comparison_operator="is not",
        context_variable=context_variable
    )
    
    print("NOT EQUALS NODE")
    return Command(
        update={
            "nodes_dicts" : [not_equals_node],
            "messages": [
                ToolMessage(
                    "Successfully added not equals node", tool_call_id=tool_call_id
                )]
        }
    )

    
@tool
def create_is_empty_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável está vazia.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    is_empty_node = create_logic_node(
        title=title,
        node_id=node_id,
        value="",
        comparison_operator="empty",
        context_variable=context_variable
    )
    
    print("IS EMPTY NODE")
    return Command(
        update={
            "nodes_dicts" : [is_empty_node],
            "messages": [
                ToolMessage(
                    "Successfully added is empty node", tool_call_id=tool_call_id
                )]
        }
    )

    
@tool
def create_not_empty_logic_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    context_variable: str
):
    """
    Cria um nó de lógica que verifica se uma variável não está vazia.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
    """
    not_empty_node = create_logic_node(
        title=title,
        node_id=node_id,
        value="",
        comparison_operator="not empty",
        context_variable=context_variable
    )
    
    print("NOT EMPTY NODE")
    return Command(
        update={
            "nodes_dicts" : [not_empty_node],
            "messages": [
                ToolMessage(
                    "Successfully added not empty node", tool_call_id=tool_call_id
                )]
        }
    )

    
def write_dify_yaml(state: DifyState):
    yaml_dify = state["metadata_dict"]  
    yaml_dify["workflow"]["graph"]["nodes"].extend(state["nodes_dicts"])
    yaml_dify["workflow"]["graph"]["edges"].extend(state["edges_dicts"])

    file = Path(YAML_PATH)
    with open(file, "w") as outfile:
        yaml.dump(yaml_dify, outfile, default_flow_style=False, allow_unicode=True)
