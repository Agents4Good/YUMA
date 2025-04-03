import yaml
from pathlib import Path
import threading

semaphore = threading.Semaphore(1)

def insert_node_yaml(file: str, node: dict):
    semaphore.acquire()
    file = Path(file)
    with open(file, "r") as infile:
        data = yaml.safe_load(infile)

    data["workflow"]["graph"]["nodes"].append(node)

    with open(file, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    semaphore.release()


def insert_edge_yaml(file: str, edge: dict):
    semaphore.acquire()
    file = Path(file)
    with open(file, "r") as infile:
        data = yaml.safe_load(infile)

    data["workflow"]["graph"]["edges"].append(edge)

    with open(file, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    semaphore.release()
        

def create_logic_node(title: str, id: str, value: str, comparison_operator: str, context_variable: str) -> dict:
    logic_node = {
        "id": id,
        "type": "custom",
        "data": {
            "cases": [
                {
                    "case_id": "true",
                    "conditions": [
                        {
                            "comparison_operator": comparison_operator,
                            "value": value,
                            "varType": "string",
                            "variable_selector": [
                                context_variable.split(".")[0],
                                context_variable.split(".")[1],
                            ]
                            if context_variable
                            else []
                        }
                    ],
                    "logical_operator": "and"
                }
            ],
            "desc": "",
            "title": title,
            "type": "if-else"
        }
    }
    return logic_node
