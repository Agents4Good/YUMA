# Documentação da Função `make_handoff_tool`

## Descrição
A função `make_handoff_tool` cria uma ferramenta que permite a transferência de uma interação para outro agente via um comando.

## Assinatura
```python
def make_handoff_tool(*, agent_name: str):
```

## Parâmetros
- `agent_name` (str): Nome do agente para o qual a transferência será realizada.

## Funcionalidade
A função cria dinamicamente um nome de ferramenta no formato `transfer_to_<agent_name>`. Em seguida, define uma ferramenta decorada com `@tool(tool_name)`, que executa a transferência chamando outro agente.

A ferramenta `handoff_to_agent` faz o seguinte:
1. Gera uma mensagem de ferramenta indicando que a transferência foi realizada com sucesso.
2. Retorna um comando `Command` que:
   - Navega para o agente especificado (`goto=agent_name`) dentro do grafo PAI.
   - Atualiza o estado incluindo o histórico de mensagens e adiciona a mensagem de ferramenta.

## Exemplo de Uso
```python
handoff_tool = make_handoff_tool(agent_name="support_agent")
```

## Observação
- A função faz uso de anotações `Annotated` para injetar o estado e o ID da chamada da ferramenta.
- O comando resultante atualiza o estado para manter a consistência do histórico da conversa.

