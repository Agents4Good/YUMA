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
        

def create_logic_node(title: str, node_id: str, value: str, comparison_operator: str, context_variable: str) -> dict:
    logic_node = {
        "id": node_id,
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

# Estrutura básica de um nó HTTP no dify, existem variações com tratamento de erro também
def create_http_node(node_id: str,
                    title: str,
                    authorization_config: dict,
                    authorization_type: str, 
                    body: dict,
                    body_type: str,
                    headers: dict,
                    method: str,
                    params: dict,
                    retry_enabled: bool = False,
                    url: str = "",
                    variables: dict = None
                    ) -> dict:
    http_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "authorization": {
                "config": authorization_config,
                "type": authorization_type
            },
            "body": {
                "data":body,
                "type": body_type
            },
            "desc": "",
            "headers": headers,
            "method": method,
            "params": params,
            "retry_config": {
                "max_retries": 3,
                "retry_enabled": retry_enabled,
                "retry_interval": 100
            },
            "timeout": {
                "max_connect_timeout": 0,
                "max_read_timeout": 0,
                "max_write_timeout": 0
            },
            "title": title,
            "type": "http-request",
            "url": url,
            "variables": variables
        }
    }

    return http_node