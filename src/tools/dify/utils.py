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
        ],
    },
    "tavily_search": {
        "type": "constant",
        "value": [
            {
                "enabled": True,
                "extra": {
                    "description": "A search engine tool built specifically for AI agents (LLMs), delivering real-time, accurate, and factual results at speed."
                },
                "parameters": {
                    "days": {"auto": 1},
                    "query": {"auto": 1},
                    "search_depth": {"auto": 1},
                    "time_range": {"auto": 1},
                    "topic": {"auto": 1},
                },
                "provider_name": "langgenius/tavily/tavily",
                "schemas": [
                    {
                        "auto_generate": None,
                        "form": "llm",
                        "human_description": {
                            "pt_BR": "The search query you want to execute with Tavily."
                        },
                        "label": {"pt_BR": "Query"},
                        "llm_description": "The search query.",
                        "name": "query",
                        "options": [],
                        "required": True,
                        "type": "string",
                    },
                    {
                        "auto_generate": None,
                        "default": "basic",
                        "form": "llm",
                        "human_description": {"pt_BR": "The depth of the search."},
                        "label": {"pt_BR": "Search Depth"},
                        "llm_description": "The depth of the search. 'basic' for standard search, 'advanced' for more comprehensive results.",
                        "name": "search_depth",
                        "options": [
                            {"label": {"pt_BR": "Basic"}, "value": "basic"},
                            {"label": {"pt_BR": "Advanced"}, "value": "advanced"},
                        ],
                        "required": False,
                        "type": "select",
                    },
                    {
                        "auto_generate": None,
                        "default": "general",
                        "form": "llm",
                        "human_description": {"pt_BR": "The category of the search."},
                        "label": {"pt_BR": "Topic"},
                        "llm_description": "The category of the search. Options include 'general', 'news', or 'finance'.",
                        "name": "topic",
                        "options": [
                            {"label": {"pt_BR": "General"}, "value": "general"},
                            {"label": {"pt_BR": "News"}, "value": "news"},
                            {"label": {"pt_BR": "Finance"}, "value": "finance"},
                        ],
                        "required": False,
                        "type": "select",
                    },
                    {
                        "auto_generate": None,
                        "default": 3,
                        "form": "llm",
                        "human_description": {
                            "pt_BR": 'The number of days back from the current date to include in the search results (only applicable when "topic" is "news").'
                        },
                        "label": {"pt_BR": "Days"},
                        "llm_description": 'The number of days back from the current date to include in the search results. Only applicable when "topic" is "news".',
                        "min": 1,
                        "name": "days",
                        "options": [],
                        "required": False,
                        "type": "number",
                    },
                    {
                        "auto_generate": None,
                        "default": "not_specified",
                        "form": "llm",
                        "human_description": {
                            "pt_BR": "The time range back from the current date to filter results."
                        },
                        "label": {"pt_BR": "Time Range"},
                        "llm_description": "The time range back from the current date to filter results. Options include 'not_specified', 'day', 'week', 'month', or 'year'.",
                        "name": "time_range",
                        "options": [
                            {
                                "label": {"pt_BR": "Not Specified"},
                                "value": "not_specified",
                            },
                            {"label": {"pt_BR": "Day"}, "value": "day"},
                            {"label": {"pt_BR": "Week"}, "value": "week"},
                            {"label": {"pt_BR": "Month"}, "value": "month"},
                            {"label": {"pt_BR": "Year"}, "value": "year"},
                        ],
                        "required": False,
                        "type": "select",
                    },
                    {
                        "auto_generate": None,
                        "default": 5,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "The maximum number of search results to return."
                        },
                        "label": {"pt_BR": "Max Results"},
                        "llm_description": "The maximum number of search results to return. Range is 1-20.",
                        "max": 20,
                        "min": 1,
                        "name": "max_results",
                        "options": [],
                        "required": False,
                        "type": "number",
                    },
                    {
                        "auto_generate": None,
                        "default": 0,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "Include a list of query-related images in the response."
                        },
                        "label": {"pt_BR": "Include Images"},
                        "llm_description": "When set to true, includes a list of query-related images in the response.",
                        "name": "include_images",
                        "options": [],
                        "required": False,
                        "type": "boolean",
                    },
                    {
                        "auto_generate": None,
                        "default": 0,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "When include_images is True, adds descriptive text for each image."
                        },
                        "label": {"pt_BR": "Include Image Descriptions"},
                        "llm_description": "When include_images is True and this is set to true, adds descriptive text for each image.",
                        "name": "include_image_descriptions",
                        "options": [],
                        "required": False,
                        "type": "boolean",
                    },
                    {
                        "auto_generate": None,
                        "default": 0,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "Include a short answer to the original query in the response."
                        },
                        "label": {"pt_BR": "Include Answer"},
                        "llm_description": "When set to true, includes a short answer to the original query in the response.",
                        "name": "include_answer",
                        "options": [],
                        "required": False,
                        "type": "boolean",
                    },
                    {
                        "auto_generate": None,
                        "default": 0,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "Include the cleaned and parsed HTML content of each search result."
                        },
                        "label": {"pt_BR": "Include Raw Content"},
                        "llm_description": "When set to true, includes the cleaned and parsed HTML content of each search result.",
                        "name": "include_raw_content",
                        "options": [],
                        "required": False,
                        "type": "boolean",
                    },
                    {
                        "auto_generate": None,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "A comma-separated list of domains to specifically include in the search results."
                        },
                        "label": {"pt_BR": "Include Domains"},
                        "llm_description": "A comma-separated list of domains to specifically include in the search results.",
                        "name": "include_domains",
                        "options": [],
                        "required": False,
                        "type": "string",
                    },
                    {
                        "auto_generate": None,
                        "form": "form",
                        "human_description": {
                            "pt_BR": "A comma-separated list of domains to specifically exclude from the search results."
                        },
                        "label": {"pt_BR": "Exclude Domains"},
                        "llm_description": "A comma-separated list of domains to specifically exclude from the search results.",
                        "name": "exclude_domains",
                        "options": [],
                        "required": False,
                        "type": "string",
                    },
                ],
                "settings": {
                    "exclude_domains": {"value": None},
                    "include_answer": {"value": 0},
                    "include_domains": {"value": None},
                    "include_image_descriptions": {"value": 0},
                    "include_images": {"value": 0},
                    "include_raw_content": {"value": 0},
                    "max_results": {"value": 5},
                },
                "tool_description": "A search engine tool built specifically for AI agents (LLMs), delivering real-time, accurate, and factual results at speed.",
                "tool_label": "Tavily Search",
                "tool_name": "tavily_search",
                "type": "builtin",
            }
        ],
    },
}
