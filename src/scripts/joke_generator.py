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
    "Quero um sistema com dois agentes que gere piadas a partir de um tópico do usuário.\n" +
    "Um agente deve receber do usuário um tópico e gerar uma pergunta no formato: 'por que a galinha atravessou a rua?'\n" +
    "com base no tópico fornecido. O outro agente deve responder à pergunta gerada pelo primeiro agente " +
    "com uma resposta engraçada e que faça sentido com o tópico abordado.\n" +
    "A saída deve possuir tanto a pergunta do primeiro agente como a resposta do segundo."
)
process.stdin.flush()

time.sleep(1)
process.stdin.write(
    "1 - O sistema deve apenas gerar piadas a partir do tópico do usuário. " +
    "2 - Todos os tipos de usuários podem usar. " +
    "3 - O usuário pode escolher qualquer tópico. " +
    "4 - Use a geração de YAML para Dify. " +
    "5 - O sistema deve possuir um nó de entrada, dois nós de agentes e um nó final de resposta.\n"
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
