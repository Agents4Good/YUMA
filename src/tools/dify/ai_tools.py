from typing import Annotated, Literal

from .utils import DIFY_AGENT_TOOLS

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.genia import write_log

LLAMA = ["claude-3-haiku-20240307", "langgenius/anthropic/anthropic"]
OPENAI = ["gpt-4", "langgenius/openai/openai"]


@tool
def create_llm_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    role: str,
    context_variable: str,
    task: str,
    temperature: float,
):
    """
    Cria um nó de chamada de LLM sem tools.

    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - role (str): Papel da LLM no workflow (exemplo: "Você é um especialista em contar piadas").
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
        - task (str): O que a LLM faz.
        - temperature (float): Criatividade do modelo, entre 0 e 1.
    """
    llm_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "context": {
                "enabled": True,
                "variable_selector": [
                    context_variable.split(".")[0],
                    context_variable.split(".")[1],
                ]
                if context_variable
                else [],
            },
            "desc": "",
            "model": {
                "completion_params": {"temperature": temperature},
                "mode": "chat",
                "name": LLAMA[0],
                "provider": LLAMA[1],
            },
            "prompt_template": [
                {"role": "system", "text": f"""{role}\n{task}"""},
                {"role": "user", "text": "{{#context#}}"}
            ],
            "title": title,
            "type": "llm",
            "variables": [],
            "vision": {"enabled": False},
        },
    }
    write_log("llm_node", llm_node)
    return Command(
        update={
            "nodes_dicts" : [llm_node],
            "messages": [
                ToolMessage(
                    "Successfully added the LLM node", tool_call_id=tool_call_id
                )]
        }
    )


@tool
def create_agent_node(
    tool_call_id: Annotated[str, InjectedToolCallId],
    title: str,
    node_id: str,
    instruction: str,
    context_variable: str,
    tool: Literal["tavily_search"],
    temperature: float,
):
    """
    Cria um nó de agente ReAct que utiliza tools para pesquisa na web, etc.

    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - instruction (str): Instrução do agente no workflow (exemplo: "Você é um agente especialista em busca de informações na web.").
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
        - tool: Literal["tavily_search"]: Ferramenta utilizada pelo agente.
        - temperature (float): Criatividade do modelo, entre 0 e 1.
    """
    agent_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "agent_parameters": {
                "instruction": {
                    "type": "constant",
                    "value": instruction + "\nUtilize obrigatoriamente a ferramenta de busca web disponível para gerar todas as respostas.\nAs respostas devem ser redigidas exclusivamente em português brasileiro.\nSempre que possível, inclua referências com links diretos para as fontes utilizadas.",
                },
                "model": {
                    "type": "constant",
                    "value": {
                        "completion_params": {
                            "temperature": temperature,
                        },
                        "mode": "chat",
                        "model": LLAMA[0],
                        "model_type": "llm",
                        "provider": LLAMA[1],
                    }
                },
                "query": {
                    "type": "constant",
                    "value": f"""{{{{#{context_variable}#}}}}"""
                },
                "tools": DIFY_AGENT_TOOLS.get(tool),
            },
            "agent_strategy_label": "FunctionCalling",
            "agent_strategy_name": "function_calling",
            "agent_strategy_provider_name": "langgenius/agent/agent",
            "desc": "",
            "title": title,
            "type": "agent",
        },
    }
    write_log("agent_node", agent_node)
    return Command(
        update={
            "nodes_dicts": [agent_node],
            "messages": [
                ToolMessage(
                    "Successfully added the agent node", tool_call_id=tool_call_id
                )
            ],
        }
    )
