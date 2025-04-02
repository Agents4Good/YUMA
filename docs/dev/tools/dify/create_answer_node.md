# Documentação da Função `create_answer_node`

## Visão Geral
A função `create_answer_node` é responsável por criar um nó de resposta dentro do grafo. Esse nó representa a etapa final da execução do grafo, onde as respostas são agregadas e formatadas para serem exibidas ao usuário.

## Assinatura da Função
```python
@tool
def create_answer_node(title: str, id: str, answer_variables: list[str])
```

## Parâmetros
- `title` (str): O nome do nó de resposta.
- `id` (str): Um identificador exclusivo baseado no nome, contendo apenas letras minúsculas e sem caracteres especiais.
- `answer_variables` (list[str]): Uma lista de strings que representa as variáveis de resposta, como `llm1.text`, `llm2.text`, etc.

## Funcionamento
A função cria um dicionário contendo os dados do nó de resposta, estruturado da seguinte maneira:

```python
answer_node = {
    "id": id,
    "type": "custom",
    "data": {
        "answer": "".join(["{{#" + f"{variable}" + "#}}\n" for variable in answer_variables]).strip(),
        "desc": "",
        "title": title,
        "type": "answer",
        "variables": [],
    },
}
```

O campo `answer` é gerado concatenando as variáveis de resposta em um formato de template com `{{#variable#}}`, separando cada uma delas por uma nova linha.

## Controle de Concorrência
A função utiliza um mecanismo de controle de concorrência com um semáforo para garantir que o nó seja inserido de forma segura no arquivo YAML:

```python
print("ANSWER NODE")
semaphore.acquire()
insert_node_yaml(YAML_PATH, answer_node)
semaphore.release()
```

## Observações
- A função assume que o arquivo YAML já existe e está localizado em `YAML_PATH`.
- A função não possui retorno explícito. Ela insere o nó gerado em um arquivo YAML através da função `insert_node_yaml`.