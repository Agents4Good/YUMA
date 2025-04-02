# Documentação da Função `create_edges`

## Visão Geral
A função `create_edges` é responsável por criar uma aresta entre dois nós. Essa aresta representa uma conexão entre um nó de origem e um nó de destino, permitindo o fluxo de informação entre eles.

## Assinatura da Função
```python
@tool
def create_edges(id: str, source_id: str, target_id: str)
```

## Parâmetros
- `id` (str): Um identificador exclusivo baseado no nome, contendo apenas letras minúsculas e sem caracteres especiais.
- `source_id` (str): O identificador do nó de origem da aresta.
- `target_id` (str): O identificador do nó de destino da aresta.

## Funcionamento
A função cria um dicionário representando a aresta com a seguinte estrutura:

```python
edge = {
    "id": id,
    "source": source_id,
    "target": target_id,
    "type": "custom"
}
```

Esse dicionário define a conexão entre os nós `source_id` e `target_id`, sendo armazenado no arquivo YAML.

## Inserção no YAML
A função insere a aresta criada no arquivo YAML usando a função `insert_edge_yaml`:

```python
insert_edge_yaml(YAML_PATH, edge)
```

## Exemplo de Uso
```python
create_edges(
    id="aresta_1",
    source_id="nodo_inicial",
    target_id="nodo_final"
)
```
Esse exemplo cria uma aresta identificada como "aresta_1", conectando os nós "nodo_inicial" e "nodo_final".