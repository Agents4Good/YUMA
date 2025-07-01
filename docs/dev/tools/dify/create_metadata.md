# Documentação da Função `create_yaml_and_metadata`

## Descrição
A função `create_yaml_and_metadata` cria um arquivo YAML e insere metadados com base no nome e na descrição fornecidos.

## Assinatura
```python
def create_yaml_and_metadata(name: str, descritption: str):
```

## Parâmetros
- `name` (str): Nome do workflow.
- `descritption` (str): Descrição do workflow.
## Funcionalidade
A função cria um dicionário `metadata` contendo informações iniciais para o arquivo do dify e workflow, incluindo:
- Nome e descrição do workflow.
- Modo padrão "advanced-chat".
- Versão padronizada "0.1.5".
- Estrutura do workflow (variáveis de conversação e ambiente, grafo de nós e arestas).

Esse dicionário é então salvo como um arquivo YAML, que posteriomente será adicionado os nós e as arestas.

## Exemplo de Uso
```python
create_yaml_and_metadata("MeuWorkflow", "Este é um workflow de exemplo.")
```

Isso gerará um arquivo YAML contendo os metadados correspondentes.

## Observação
A variável `YAML_PATH` é definida como padrão no código fonte e deve ser ajustada conforme necessário.

