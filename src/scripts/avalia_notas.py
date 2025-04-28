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
    "Preciso de um sistema automatizado para avaliar alunos em uma atividade escolar, dividido em quatro etapas: " + 
    "1. A primeira etapa recebe uma pergunta objetiva contendo a nota do aluno, como por exemplo: " +
        "'O aluno foi aprovado na atividade? Nota: 7.7'" +
        "Com base na regra de que a nota mínima para aprovação é 7.0, o sistema deve interpretar a nota e responder apenas com 'sim' ou 'não'. " + 
    "2. Se a resposta for 'sim', o sistema avança para a segunda etapa, que retorna a mensagem: " +
        "'Aprovado na atividade'. " + 
    "3. Se a resposta for 'não', o sistema segue para a terceira etapa, que retorna a mensagem: 'Reprovado na atividade'. " + 
    "4. Após a avaliação, o resultado final do aluno deve ser respondido para o usuário visualizar.\n",
    
    "1 - verificar a aprovação dos alunos. " +
    "2 - qualquer pessoa. " + 
    "3 - apenas a verficação da afirmação. " + 
    "4 - utilize a serialização do dify para yaml. " +
    "5 - nenhum.\n",
    
    "Prossiga para o arquiteto.\n",
    "Prossiga.\n",
    "q\n",
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
