# Documentação da Função `create_start_node`

## Descrição
A função `create_start_node` cria o nó inicial do grafo do dify, representando a primeira etapa a ser executada e onde sera recebido a entrada do usuário. Esse nó é inserido em no arquivo YAML que será upado no dify.

## Assinatura
```python
def create_start_node(title: str, id: str):
```

## Parâmetros
- `title` (str): Nome do nó inicial.
- `id` (str): Identificador único do nó, baseado no nome, convertido para minúsculas e sem caracteres especiais.

## Funcionalidade
1. Cria um dicionário `start_node` contendo:
   - `id`: Identificador do nó.
   - `type`: Tipo do nó (definido como "custom").
   - `data`: Contém informações adicionais, incluindo:
     - `title`: Nome do nó.
     - `type`: Definido como "start".
     - `variables`: Lista vazia para armazenar variáveis futuras.
2. Exibe "START NODE" no console.
3. Utiliza um semáforo para garantir acesso exclusivo ao arquivo YAML durante a inserção do nó:
   - `semaphore.acquire()`: Bloqueia o recurso para evitar concorrência.
   - `insert_node_yaml(YAML_PATH, start_node)`: Insere o nó no arquivo YAML.
   - `semaphore.release()`: Libera o recurso após a inserção.
