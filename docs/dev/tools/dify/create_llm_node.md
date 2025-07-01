# Documentação da Função `create_llm_node`

## Descrição
A função `create_llm_node` cria um nó para interações com um modelo de linguagem (LLM) dentro do workflow. Esse nó pode processar prompts e compartilhar variáveis de contexto com outros nós.

## Assinatura
```python
@tool
def create_llm_node(
    id: str,
    title: str,
    prompt: str,
    temperature: float = 0.7,
    context_variable: str = "",
):
```

## Parâmetros
- `id` (str): Identificador único do nó, baseado no nome, convertido para minúsculas e sem caracteres especiais.
- `title` (str): Nome do nó.
- `prompt` (str): Texto do prompt utilizado para a interação com o modelo.
- `temperature` (float, opcional, default=0.7): Controla a aleatoriedade das respostas do modelo.
- `context_variable` (str, opcional, default=""): Variável compartilhada entre os nós do workflow. Pode ter dois formatos:
  1. `sys.query`: Entrada do usuário.
  2. `<previous_node_id>.text`: Saída do nó anterior.
  
  **Restrição**: Um nó pode ter apenas uma variável de contexto.

## Funcionalidade
1. Cria um dicionário `llm_node` contendo:
   - `id`: Identificador do nó.
   - `type`: Definido como "custom".
   - `data`: Contém informações sobre o modelo e contexto:
     - `context`: Habilita a variável de contexto, dividida entre ID do nó e o tipo da variável.
     - `model`: Define o modelo utilizado (`gpt-4` via `langgenius/openai/openai`).
     - `prompt_template`: Define o prompt enviado ao modelo.
     - `vision`: Desabilita o suporte a entrada visual.
2. Exibe "LLM NODE" no console.
3. Utiliza um semáforo para garantir acesso exclusivo ao arquivo YAML durante a inserção do nó:
   - `semaphore.acquire()`: Bloqueia o recurso para evitar concorrência.
   - `insert_node_yaml(YAML_PATH, llm_node)`: Insere o nó no arquivo YAML.
   - `semaphore.release()`: Libera o recurso após a inserção.

## Exemplo de Uso
```python
create_llm_node(
    id="analise_texto",
    title="Análise de Texto",
    prompt="Analise o seguinte texto e forneça insights...",
    temperature=0.5,
    context_variable="sys.query",
)
```

## Observação
- O modelo utilizado é fixo (gpt-4) e fornecido por langgenius/openai/openai.