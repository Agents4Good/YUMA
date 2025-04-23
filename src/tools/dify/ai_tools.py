from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command


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
    Cria um nó de agente (LLM) para um workflow multiagente.
    
    Parâmetros:
        - title (str): Nome do nó.
        - node_id (str): Identificador único baseado no nome (minúsculas, sem caracteres especiais).
        - role (str): Papel do agente no workflow (exemplo: "Você é um especialista em contar piadas").
        - context_variable (str): Variável de contexto compartilhada entre nós (exemplo: use "sys.query" para receber o contexto do nó inicial, "<previous_node_id>.text" para receber o contexto de outros nós).
        - task (str): O que o agente faz. Para receber os dados do nó anterior use exatamente "{{#context#}}". (exemplo: "Seu trabalho é responder a pergunta: "{{#context#}}").
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
                "name": "claude-3-haiku-20240307",
                "provider": "langgenius/anthropic/anthropic",
            },
            "prompt_template": [{"role": "system", "text": f"""{role}\n{task}"""}],
            "title": title,
            "type": "llm",
            "variables": [],
            "vision": {"enabled": False},
        },
    }
    print("LLM NODE")
    return Command(
        update={
            "nodes_dicts" : [llm_node],
            "messages": [
                ToolMessage(
                    "Successfully added the LLM node", tool_call_id=tool_call_id
                )]
        }
    )
