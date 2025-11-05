from typing import List
from langgraph.types import Command

from agentshub.dify.node_creation import (
    create_start_node,
    create_llm_node,
    create_answer_node,
    create_start_with_logic_node,
    create_end_with_logic_node,
    create_contains_logic_node,
    create_not_contains_logic_node,
    create_is_equals_logic_node,
    create_not_equals_logic_node,
    create_is_empty_logic_node,
    create_not_empty_logic_node,
    create_http_node,
    create_agent_node,
    create_extractor_document_node,
)

from agentshub.dify.edge_creator import (
    create_edges,
    create_logic_edges,
)

from schema.dify import DifyState
from utils.yuma import write_log


tools_dify = {
    "create_llm_node": create_llm_node,
    "create_agent_node": create_agent_node,
    "create_answer_node": create_answer_node,
    "create_start_node": create_start_node,
    "create_start_with_logic_node": create_start_with_logic_node,
    "create_end_with_logic_node": create_end_with_logic_node,
    "create_contains_logic_node": create_contains_logic_node,
    "create_not_contains_logic_node": create_not_contains_logic_node,
    "create_is_equals_logic_node": create_is_equals_logic_node,
    "create_not_equals_logic_node": create_not_equals_logic_node,
    "create_is_empty_logic_node": create_is_empty_logic_node,
    "create_not_empty_logic_node": create_not_empty_logic_node,
    "create_edges": create_edges,
    "create_logic_edges": create_logic_edges,
    "create_http_node": create_http_node,
    "create_extractor_document_node": create_extractor_document_node
}


def call_dify_tools(state: DifyState) -> List[Command]:
    tool_calls = []
    i = -1
    while True:
        message = state["messages"][i]
        tool_call = getattr(message, "tool_calls", [])
        if tool_call != []:
            tool_calls.extend(tool_call)
        else:
            break
        i -= 1

    write_log("call_dify_tools - all tool_calls", tool_calls)
    commands = []
    for tool_call in tool_calls:
        commands.append(tools_dify[tool_call["name"]].invoke(tool_call))

    return commands
