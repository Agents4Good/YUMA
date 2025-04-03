import yaml
import os


from state import DifyState
from typing import Annotated, Literal

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from utils.plantuml_parser import generate_diagram, json_to_plantuml
from utils.tools_utils import insert_node_yaml, insert_edge_yaml
import threading
from pathlib import Path

YAML_PATH = os.path.join("generated_files", "dify.yaml")
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
    # with open(YAML_PATH, "w") as outfile:
    #     yaml.dump(metadata, outfile, default_flow_style=False, allow_unicode=True)


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
    # semaphore.acquire()
    # insert_node_yaml(YAML_PATH, start_node)
    # semaphore.release()



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
        - task (str): Tarefa do agente. Use exatamente "{{#context#}}" para inserir contexto na resposta. (exemplo: "Seu trabalho é responder a pergunta: "{{#context#}}").
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
                "name": "gpt-4",
                "provider": "langgenius/openai/openai",
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
    # semaphore.acquire()
    # insert_node_yaml(YAML_PATH, llm_node)
    # semaphore.release()


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
    # semaphore.acquire()
    # insert_node_yaml(YAML_PATH, answer_node)
    # semaphore.release()


@tool
def create_edges(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    id: str, source_id: str, target_id: str):
    """
    Cria uma aresta entre dois nós no workflow.
    
    Parâmetros:
        - edge_id (str): Identificador único da aresta (minúsculas, sem caracteres especiais).
        - source_id (str): ID do nó de origem da aresta (exemplo: "start_node", "llm1").
        - target_id (str): ID do nó de destino da aresta (exemplo: "answer_node", "llm2").
    """
    edge = {"id": id, "source": source_id, "target": target_id, "type": "custom"}
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

    # semaphore.acquire()
    # insert_edge_yaml(YAML_PATH, edge)
    # semaphore.release()

def write_dify_yaml(state: DifyState):
    yaml_dify = state["metadata_dict"]  
    yaml_dify["workflow"]["graph"]["nodes"].extend(state["nodes_dicts"])
    yaml_dify["workflow"]["graph"]["edges"].extend(state["edges_dicts"])

    file = Path(YAML_PATH)
    with open(file, "w") as outfile:
        yaml.dump(yaml_dify, outfile, default_flow_style=False, allow_unicode=True)

    

# create_yaml_and_metadata(
#                          "Contador de piadas",
#                          "Um contador de piadas que conta piadas engraçadas.")

# create_start_node( "Início", "start")

# create_llm_node(
#                 "llm1",
#                 "Criador de Perguntas",
#                 """Seu trabalho é gerar o início de uma piada que mais tarde será encaminhada para outro agente que a completará.
# O tema da piada é: "{{#context#}}"
# As piadas devem ser estruturadas em forma de pergunta, por exemplo:
# "O que é um ponto preto em cima do castelo?""",
#                 1.0,
#                 "sys.query")

# create_llm_node(
#                 "llm2",
#                 "Criador de respostas",
#                 """Seu trabalho é responder a pergunta: "{{#context#}}"  em forma de piada, de maneira engraçada e que faça sentido com o tópico abordado.
# Retorne apenas a resposta da pergunta, nada mais.""",
#                 1.0,
#                 "llm1.text"
#                 )

# create_answer_node(
#                    "Fim",
#                    "end",
#                    """{{#llm1.text#}}\n{{#llm2.text#}}""")

# create_edges( "edge1", "start", "llm1")
# create_edges( "edge2", "llm1", "llm2")
# create_edges( "edge3", "llm2", "end")
