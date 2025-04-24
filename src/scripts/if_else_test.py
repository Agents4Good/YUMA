import subprocess
import time
import sys
import os

# Definição do caminho para o Python e do script a ser executado
python_executable = sys.executable
SRC_PATH = os.path.abspath(os.curdir)
MAIN_PATH = os.path.join(SRC_PATH, 'main.py')

# Inicia o subprocesso para executar o script main.py
process = subprocess.Popen(
    [python_executable, MAIN_PATH],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Entradas simulando a interação via input()
inputs = [
    "Preciso de um sistema com 3 agentes no qual eu envio uma afirmação para um agente e ele responde apenas com 'sim' ou 'não'. " + 
    "Caso a resposta dele seja sim, o sistema segue para o segundo agente que, ao receber o 'sim', responde com 'Verdadeiro'. " +
    "Caso o primeiro agente responda 'não', segue para o terceiro que, ao receber o 'não', responde com 'Falso'.\n",

    "1 - verificar a veracidade das afirmações. " +
    "2 - qualquer pessoa. " +
    "3 - apenas a verificação da afirmação. " +
    "4 - utilize a serialização do Dify para YAML. " +
    "5 - nenhum. " +
    "6 - encaminhar para o nó final.\n",

    "Prossiga para o arquiteto.\n",
    "Prossiga\n",
    "Prossiga.\n",
    "q\n"
]

# Escreve cada entrada com delay e flush
for entrada in inputs:
    process.stdin.write(entrada)
    process.stdin.flush()
    time.sleep(1)

# Fecha stdin para informar fim de entrada
process.stdin.close()

# Lê a saída do stdout
print("Saída do programa:")
for linha in process.stdout:
    print(linha, end='')

# Lê erros se houverem
erros = process.stderr.read()
if erros:
    print("\nErros:")
    print(erros)
