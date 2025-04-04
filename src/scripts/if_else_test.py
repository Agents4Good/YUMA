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
    "Preciso de um sistema com 3 agentes no qual eu envio uma afirmação para um agente e ele responde apenas com 'sim' ou 'não'.\n" +
    "Caso a resposta dele seja sim, o sistema segue para o segundo agente que, ao receber o 'sim', responde com 'Verdadeiro'.\n" +
    "Caso o primeiro agente responda 'não', segue para o terceiro que, ao receber o 'não', responde com 'Falso'.\n"
)
process.stdin.flush()

time.sleep(1)
process.stdin.write(
    "1 - verificar a veracidade das afirmações. " +
    "2 - qualquer pessoa. " +
    "3 - apenas a verficação da afirmação. " +
    "4 - utilize a serializaçãodo dify para yaml. " +
    "5 - nenhum. " +
    "6 - encaminhar para o nó final.\n"
)
process.stdin.flush()

time.sleep(1)
process.stdin.write("Prossiga para o arquiteto.\n")
process.stdin.flush()

time.sleep(1)
process.stdin.write("Prossiga\n")
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
