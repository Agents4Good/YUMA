from typing import Annotated, Literal

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.yuma import write_log


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
    edge = {"id": edge_id, "source": source_id,
            "target": target_id, "type": "custom"}

    write_log("create_edges", edge)
    return Command(
        update={
            "edges_dicts": [edge],
            "messages": [
                ToolMessage(
                    f"Successfully added the edge between {source_id} and {target_id}",
                    tool_call_id=tool_call_id,
                )
            ],
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
        - source_id (str): ID do nó de lógica que está sendo conectado (exemplo: "start_with_node").
        - source_handle (Literal["true", "false"]): Indica se a aresta é para o caminho "true" ou "false" do nó de lógica.
        - target_id (str): ID do nó de destino da aresta (exemplo: "llm1", "llm2").
    """
    logic_edge = {"id": edge_id, "source": source_id,
                  "sourceHandle": source_handle, "target": target_id, "type": "custom"}

    write_log("create_logic_edges", logic_edge)
    return Command(
        update={
            "edges_dicts": [logic_edge],
            "messages": [
                ToolMessage(
                    f"Successfully added logic edge between {source_id} and {target_id}", tool_call_id=tool_call_id
                )]
        }
    )
