import yaml
from schema.dify import DifyState
from langgraph.types import Command
from langchain_core.messages import SystemMessage
from typing import List
from pathlib import Path
from utils.yuma import get_generated_files_path, write_log
from utils.dify import dify_import_yaml

YAML_PATH = get_generated_files_path("dify.yaml")


def _write_dify_yaml(state: DifyState):
    yaml_dify = state["metadata_dict"]
    yaml_dify["workflow"]["graph"]["nodes"].extend(state["nodes_dicts"])
    yaml_dify["workflow"]["graph"]["edges"].extend(state["edges_dicts"])

    file = Path(YAML_PATH)
    if file.exists():
        file.unlink()
        
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