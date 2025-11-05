from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.yuma import write_log


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
        "data": {"desc": "",
                 "title": title,
                 "type": "start",
                 "variables": [
                     {"allowed_file_types": ["document"],
                      "allowed_file_upload_methods": ["local_file", "remote_url"],
                      "label": "files",
                      "max_length": 5,
                      "required": False,
                      "type": "file-list",
                      "variable": "files"}]
                 }
    }

    write_log("create_start_node", start_node)
    return Command(
        update={
            "nodes_dicts": [start_node],
            "messages": [
                ToolMessage(
                    "Successfully added the start node", tool_call_id=tool_call_id
                )]
        }
    )
