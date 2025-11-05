from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.yuma import write_log


@tool
def create_extractor_document_node(
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
    extractor_document_node = {
        "id": node_id,
        "type": "custom",
        "data": {"desc": "",
                 "title": title, 
                 "type": "document-extractor", 
                 "variables":['files']
                }
        }
    
    write_log("create_extractor_document_node", extractor_document_node)
    return Command(
        update={
            "nodes_dicts" : [extractor_document_node],
            "messages": [
                ToolMessage(
                    "Successfully added the start node", tool_call_id=tool_call_id
                )]
        }
    )