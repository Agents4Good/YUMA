import subprocess
import time
import sys

python_executable = sys.executable

process = subprocess.Popen(
    [python_executable, "main.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(1)
process.stdin.write(
    "Quero um sistema multiagentes que gere piadas a partir de um tópico do usuário. " +
    "Um agente deve gerar piadas pergunta e o outro agente deve respondê-las.\n"
)
process.stdin.flush()

time.sleep(1)
process.stdin.write(
    "O sistema deve apenas gerar piadas a partir do tópico do usuário. " +
    "Todos os tipos de usuários podem usar. " + 
    "Use Python + CLI. " +
    "Apenas os dois agentes devem ser usados.\n"
)
process.stdin.flush()

time.sleep(1)
process.stdin.write("Prossiga para o arquiteto.\n")
process.stdin.flush()

time.sleep(1)
process.stdin.write("Deixe apenas os agentes de gerar perguntas e o de respondê-las.\n")
process.stdin.flush()

time.sleep(1)
process.stdin.write("Prossiga.\n")
process.stdin.flush()

time.sleep(1)
process.stdin.write("q\n")
process.stdin.flush()

saida, erro = process.communicate()
print("Saída do programa:")
print(saida)

if erro:
    print("Erros:")
    print(erro)
