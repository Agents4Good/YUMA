import os
import pty
import sys
import threading
from langchain_core.messages import AIMessage
from schema.yuma import AgentState
from langgraph.types import Command
from utils.yuma import write_log
from typing import Optional
import time

import os
import subprocess
import threading
from langchain_core.messages import AIMessage
from schema.yuma import AgentState
from langgraph.types import Command
from utils.yuma import write_log
from typing import Optional

import os
import subprocess
from langchain_core.messages import AIMessage
from schema.yuma import AgentState
from langgraph.types import Command
from utils.yuma import write_log
from typing import Optional

def code_validator(state: AgentState) -> Optional[Command]:
    try:
        mensagens = state.get("messages", [])
        ultima_msg = next((msg.content for msg in reversed(mensagens) if isinstance(msg, AIMessage)), "")

        if not ultima_msg:
            msg_erro = "Nenhuma mensagem AI encontrada para construir o prompt de validação."
            write_log("code_validator", msg_erro)
            state["messages"].append(AIMessage(content=msg_erro))
            return Command(update=state, goto="next_node")

        prompt_execucao = """
        O código de um agente inteligente foi gerado nessa pasta.
        Instale as dependencias e execute o projeto conforme o que for necessário.
        Se o input inicial for iterativo, altere o código para receber um valor hardcoded para que você possa executar.
        Execute o projeto conforme instruções (exemplo: 'python3 main.py').
        Capture a saída da execução e informe se houve erros.
        A chave OPENAI_API_KEY está armazenada no terminal, você pode executar o sistema que ela será lida automaticamente.
        Se o sistema for executado corretamente, retorne SUCCESS_EXECUTION. Caso não seja executado corretamente, retorne FAIL_EXECUTION.
        """

        gemini_path = "/tmp/gemini_files"
        max_retries = 3
        attempt = 0
        output_text = ""

        while attempt < max_retries:
            attempt += 1
            write_log("code_validator", f"Tentativa {attempt} de execução do Gemini CLI...")

            try:
                process = subprocess.Popen(
                    ["gemini", "-y", "--model", "gemini-2.5-flash", "-p", prompt_execucao],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=gemini_path,
                    bufsize=1
                )

                output_lines = process.stdout.readlines()
                output_text = "".join(output_lines)
                print(output_text)

                # Se o comando foi bem sucedido, interrompe o retry
                if "SUCCESS_EXECUTION" in output_text:
                    break

            except Exception as e:
                write_log("code_validator", f"Erro na tentativa {attempt}: {str(e)}")

        goto = "human_node"
        if "SUCCESS_EXECUTION" in output_text:
            msg_sucesso = f"Validação executada com sucesso:\n{output_text}"
            write_log("code_validator", msg_sucesso)
            state["messages"].append(AIMessage(content=msg_sucesso))
        else:
            msg_erro = f"Erro na execução da validação após {attempt} tentativas:\n{output_text}"
            write_log("code_validator", msg_erro)
            state["messages"].append(AIMessage(content=msg_erro))
            goto = "code_generator"

        return Command(update=state, goto=goto)

    except Exception as e:
        msg_exc = f"Erro inesperado na validação Gemini CLI: {str(e)}"
        write_log("code_validator", msg_exc)
        state["messages"].append(AIMessage(content=msg_exc))
        return Command(update=state, goto="code_generator")
