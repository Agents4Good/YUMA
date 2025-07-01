import subprocess
import time
import sys
import os

python_executable = sys.executable
SRC_PATH = os.path.abspath(os.curdir)
MAIN_PATH = os.path.join(SRC_PATH, 'main.py')

process = subprocess.Popen(
    [python_executable, MAIN_PATH],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

inputs = [
    "Quero um sistema com dois agentes que gere piadas a partir de um tópico do usuário. " +
    "Um agente deve receber do usuário um tópico e gerar uma pergunta no formato: 'por que a galinha atravessou a rua?' " +
    "com base no tópico fornecido. O outro agente deve responder à pergunta gerada pelo primeiro agente " +
    "com uma resposta engraçada e que faça sentido com o tópico abordado. " +
    "A saída deve possuir tanto a pergunta do primeiro agente como a resposta do segundo.\n",

    "1 - O sistema deve apenas gerar piadas a partir do tópico do usuário. " +
    "2 - Todos os tipos de usuários podem usar. " +
    "3 - O usuário pode escolher qualquer tópico. " +
    "4 - Use a geração de YAML para Dify. " +
    "5 - O sistema deve possuir um nó de entrada, dois nós de agentes e um nó final de resposta.\n",

    "Prossiga para o arquiteto.\n",
    "Deixe apenas os agentes de gerar perguntas e o de respondê-las.\n",
    "Prossiga para a geração\n",
    "q\n"
]

for entrada in inputs:
    process.stdin.write(entrada)
    process.stdin.flush()
    time.sleep(1)

process.stdin.close()

print("Saída do programa:")
for linha in process.stdout:
    print(linha, end='')

erros = process.stderr.read()
if erros:
    print("\nErros:")
    print(erros)
