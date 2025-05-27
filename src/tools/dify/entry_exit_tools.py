from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.genia import write_log


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
    
    write_log("create_start_node", start_node)
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
def create_answer_node(
    tool_call_id: Annotated[str, InjectedToolCallId], 
    title: str, node_id: str, answer_variables: list[str]):
    """
    Cria o nó final do workflow responsável por exibir os outputs.

    Esse nó deve ser criado por último no workflow.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - answer_variables (list[str]): Lista de variáveis a serem exibidas para o usuário em ordem de disposição (exemplo: ["llm1.text", "llm2.text"]). Utilize apenas o sufixo ".text".
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
    
    write_log("create_answer_node", answer_node)
    return Command(
        update={
            "nodes_dicts" : [answer_node],
            "messages": [
                ToolMessage(
                    "Successfully added the answer node", tool_call_id=tool_call_id
                )]
        }
    )
