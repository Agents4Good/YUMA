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


def create_logic_node(
    title: str,
    node_id: str,
    value: str,
    comparison_operator: str,
    context_variable: str,
) -> dict:
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
                            "variable_selector": (
                                [
                                    context_variable.split(".")[0],
                                    context_variable.split(".")[1],
                                ]
                                if context_variable
                                else []
                            ),
                        }
                    ],
                    "logical_operator": "and",
                }
            ],
            "desc": "",
            "title": title,
            "type": "if-else",
        },
    }
    return logic_node


def create_yaml_metadata(name: str, descritption: str):
    """
    Cria os metadados do arquivo YAML.

    Parâmetros:
        - name (str): Nome do workflow.
        - description (str): Descrição do workflow.
    """
    return {
        "app": {"description": descritption, "mode": "advanced-chat", "name": name},
        "version": "0.1.5",
        "workflow": {
            "conversation_variables": [],
            "environment_variables": [],
            "graph": {"edges": [], "nodes": []},
        },
    }


DIFY_AGENT_TOOLS = {
    "web_scraper": {
        "type": "constant",
        "value": [
            {
                "enabled": True,
                "extra": {
                    "description": "Ferramenta de busca na web por links relevantes."
                },
                "parameters": {"url": {"auto": 1}},
                "provider_name": "webscraper",
                "schemas": [
                    {
                        "form": "llm",
                        "human_description": {"pt_BR": "used for linking to webpages"},
                        "label": {"pt_BR": "URL"},
                        "llm_description": "url for scraping",
                        "name": "url",
                        "options": [],
                        "required": True,
                        "type": "string",
                    },
                    {
                        "default": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36",
                        "form": "form",
                        "human_description": {
                            "pt_BR": "used for identifying the browser."
                        },
                        "label": {"pt_BR": "User Agent"},
                        "name": "user_agent",
                        "options": [],
                        "required": False,
                        "type": "string",
                    },
                    {
                        "default": "false",
                        "form": "form",
                        "human_description": {
                            "pt_BR": "If true, the crawler will only return the page summary content."
                        },
                        "label": {"pt_BR": "Whether to generate summary"},
                        "name": "generate_summary",
                        "options": [
                            {"label": {"pt_BR": "Yes"}, "value": "true"},
                            {"label": {"pt_BR": "No"}, "value": "false"},
                        ],
                        "required": False,
                        "type": "boolean",
                    },
                ],
                "settings": {
                    "generate_summary": {"value": "false"},
                    "user_agent": {
                        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36"
                    },
                },
                "tool_label": "Web Scraper",
                "tool_name": "webscraper",
                "type": "builtin",
            }
        ]
    }
}
