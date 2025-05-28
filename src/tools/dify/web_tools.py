from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.genia import write_log


@tool
def create_http_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str
):
    """
    Cria um nó HTTP que possibilita requisições .

    Parametros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
    """

    http_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "body": {
                "type": None,
                "data": []
            },
            "title": title,
            "type": "http-request"
        }
    }
    
    write_log("create_http_node", http_node)
    return Command(
        update={
            "nodes_dicts" : [http_node],
            "messages": [
                ToolMessage(
                    "Successfully added the HTTP node", tool_call_id=tool_call_id
                )]
        }
    )
