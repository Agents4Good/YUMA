import yaml
from schema.dify import DifyState
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from typing import List
from pathlib import Path
from utils.yuma import get_generated_files_path, write_log
from tools.dify import (
    create_llm_node,
    create_agent_node,
    create_answer_node,
    create_start_node,
    create_contains_logic_node,
    create_edges,
    create_logic_edges,
    create_http_node,
)
from utils.dify import dify_import_yaml

YAML_PATH = get_generated_files_path("dify.yaml")


def _write_dify_yaml(state: DifyState):
    yaml_dify = state["metadata_dict"]
    yaml_dify["workflow"]["graph"]["nodes"].extend(state["nodes_dicts"])
    yaml_dify["workflow"]["graph"]["edges"].extend(state["edges_dicts"])

    file = Path(YAML_PATH)
    with open(file, "w") as outfile:
        yaml.dump(yaml_dify, outfile,
                  default_flow_style=False, allow_unicode=True)


def dify_yaml_builder(state: DifyState) -> Command:
    _write_dify_yaml(state)
    try:
        dify_import_yaml("dify.yaml", "local")
    except Exception as e:
        print(
            "Não foi possível importar o yaml para o app Dify local, tentando importar na web"
        )
        try:
            dify_import_yaml("dify.yaml", "web")
        except Exception as e:
            write_log("dify_yaml_builder - Local Import Error", str(e))
            print("Não foi possível importar o yaml para o app Dify local")

    return Command(
        update={
            "messages": [SystemMessage(content="Successfully create the dify yaml")]
        },
    )


tools_dify = {
    "create_llm_node": create_llm_node,
    "create_agent_node": create_agent_node,
    "create_answer_node": create_answer_node,
    "create_start_node": create_start_node,
    # "create_start_with_logic_node": create_start_with_logic_node,
    # "create_end_with_logic_node": create_end_with_logic_node,
    "create_contains_logic_node": create_contains_logic_node,
    # "create_not_contains_logic_node": create_not_contains_logic_node,
    # "create_is_equals_logic_node": create_is_equals_logic_node,
    # "create_not_equals_logic_node": create_not_equals_logic_node,
    # "create_is_empty_logic_node": create_is_empty_logic_node,
    # "create_not_empty_logic_node": create_not_empty_logic_node,
    "create_edges": create_edges,
    "create_logic_edges": create_logic_edges,
    "create_http_node": create_http_node,
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
