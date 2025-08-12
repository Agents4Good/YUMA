import subprocess
import json
import os
from typing import Dict, Any
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.types import Command
from typing import Literal
from schema.yuma import AgentState
from utils.yuma import write_log


def code_generator(state: AgentState) -> Command[Literal["human_node", "code_validator"]]:
    """
    Agente que executa comandos do Gemini CLI baseado na arquitetura gerada.
    """
    try:
        # Extrair a arquitetura do estado
        architecture_output = state.get("architecture_output")
        if not architecture_output:
            write_log("gemini_cli_agent", "Nenhuma arquitetura encontrada no estado")
            return Command(update=state, goto="human_node")
        
        # Converter a arquitetura para formato JSON se necessário
        if hasattr(architecture_output, 'model_dump_json'):
            architecture_json = architecture_output.model_dump_json()
        else:
            architecture_json = json.dumps(architecture_output)
        
        # Criar o comando do Gemini CLI
        gemini_command = create_gemini_command(architecture_json)
        
        # Executar o comando
        result = execute_gemini_command(gemini_command)
        
        # Adicionar a resposta ao estado
        state["messages"].append(AIMessage(content=f"Gemini CLI executado com sucesso:\n{result}"))
        
        write_log("gemini_cli_agent", f"Comando executado: {gemini_command}")
        write_log("gemini_cli_agent", f"Resultado: {result}")
        
        return Command(update=state, goto="code_validator")
        
    except Exception as e:
        error_msg = f"Erro ao executar Gemini CLI: {str(e)}"
        write_log("gemini_cli_agent", error_msg)
        state["messages"].append(AIMessage(content=error_msg))
        return Command(update=state, goto="code_validator")

def create_gemini_command(architecture_json: str) -> list:
    architecture_json = json.loads(architecture_json)
    template = ""
    file_path = "src/agentshub/templates/conversational_agent.py" if "simple" in architecture_json['agent_type'].lower() else "src/agentshub/templates/tool_agent.py"
    with open(file_path) as f:
        template = f.read()
    prompt = f"""
    Um agente é uma entidade artificial composta por:
      - Especificações de prompt: definem seu estado inicial.
      - Histórico de conversação: representa seu estado atual.
      - Capacidade de interação com o ambiente: por meio de ferramentas ou ações.

    Abaixo segue uma arquitetura de agente:

    Arquitetura:
    {architecture_json}

    Abaixo segue um template de agente:
    {template}

    Com base na arquitetura proposta e no template, gere um código Python que implemente esta arquitetura usando o framework LangGraph.
    O código deve incluir:
    1. Definição do agente
    2. Definição do system prompt com base no agent_role e agent_task
    3. Configuração do grafo
    4. Função main para execução
    5. Tratamento de entrada/saída do usuário
    6. Leitura da variável OPENAI_API_KEY do ambiente

    Crie os arquivos necessários com o código Python que implementa essa arquitetura usando o framework LangGraph. Não explique nada, não escreva instruções, apenas imprima o código completo a partir da próxima linha.
    """
    
    return ["gemini", "-y", "--prompt", prompt]



def execute_gemini_command(command: list) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
            cwd='/tmp/gemini_files'
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Erro na execução: {' '.join(command)}\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Erro: Timeout na execução do comando Gemini CLI"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"

