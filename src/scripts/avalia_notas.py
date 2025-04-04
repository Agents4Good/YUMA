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
    (
        "Preciso de um sistema automatizado para avaliar alunos em uma atividade escolar, dividido em quatro etapas: 1. A primeira etapa recebe uma pergunta objetiva contendo a nota do aluno, como por exemplo: \"O aluno foi aprovado na atividade? Nota: 7.7\" Com base na regra de que a nota mínima para aprovação é 7.0, o sistema deve interpretar a nota e responder apenas com 'sim' ou 'não'. 2. Se a resposta for 'sim', o sistema avança para a segunda etapa, que retorna a mensagem: 'Aprovado na atividade'. 3. Se a resposta for 'não', o sistema segue para a terceira etapa, que retorna a mensagem: 'Reprovado na atividade'. 4. Após a avaliação, o resultado final do aluno deve ser respondido para o usuário visualizar."
    )
)
process.stdin.flush()

time.sleep(1)
process.stdin.write(
    "1 - verificar a aprovação dos alunos. " +
    "2 - qualquer pessoa. " +
    "3 - apenas a verficação da afirmação. " +
    "4 - utilize a serializaçãodo dify para yaml. " +
    "5 - nenhum. "
)
process.stdin.flush()

time.sleep(1)
process.stdin.write("Prossiga para o arquiteto.\n")
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
