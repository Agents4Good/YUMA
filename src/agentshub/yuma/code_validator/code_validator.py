import json
from langchain_core.messages import AIMessage
from schema.yuma import AgentState
from langgraph.types import Command
from utils.yuma import write_log
from typing import Optional
import subprocess

def code_validator(state: AgentState) -> Optional[Command]:
    """
    Valida o código gerado executando o Gemini CLI com um prompt
    que indica a execução do código (ex: rodar 'python3 main.py').
    """
    try:
        mensagens = state.get("messages", [])
        ultima_msg = ""
        for msg in reversed(mensagens):
            if isinstance(msg, AIMessage):
                ultima_msg = msg.content
                break
        
        if not ultima_msg:
            msg_erro = "Nenhuma mensagem AI encontrada para construir o prompt de validação."
            write_log("code_validator", msg_erro)
            state["messages"].append(AIMessage(content=msg_erro))
            return Command(update=state, goto="next_node")

        prompt_execucao = f"""
        O código de um agente inteligente foi gerado nessa pasta.
        Instale as dependencias e execute o projeto conforme o que for necessário.
        Se o input inicial for iterativo, altere o código para receber um valor hardcoded para que você possa executar.
        Execute o projeto conforme instruções (exemplo: 'python3 main.py').
        Capture a saída da execução e informe se houve erros.
        Se for preciso, leia a OPENAI_API_KEY das envs do sistema.
        """
        
        command =["gemini", "-y", "--prompt", prompt_execucao]

        write_log("code_validator", f"Executando validação com comando: {' '.join(command)}")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
            cwd='/tmp/gemini_files'  # ajuste conforme seu ambiente
        )

        goto = "human_node"
        if result.returncode == 0:
            msg_sucesso = f"Validação executada com sucesso:\n{result.stdout}"
            write_log("code_validator", msg_sucesso)
            state["messages"].append(AIMessage(content=msg_sucesso))
        else:
            msg_erro = f"Erro na execução da validação:\n{result.stderr}"
            write_log("code_validator", msg_erro)
            state["messages"].append(AIMessage(content=msg_erro))
            goto = "code_generator"

        return Command(update=state, goto=goto)

    except subprocess.TimeoutExpired:
        msg_timeout = "Timeout durante a execução da validação Gemini CLI."
        write_log("code_validator", msg_timeout)
        state["messages"].append(AIMessage(content=msg_timeout))
        return Command(update=state, goto="human_node")

    except Exception as e:
        msg_exc = f"Erro inesperado na validação Gemini CLI: {str(e)}"
        write_log("code_validator", msg_exc)
        state["messages"].append(AIMessage(content=msg_exc))
        return Command(update=state, goto="code_generator")
