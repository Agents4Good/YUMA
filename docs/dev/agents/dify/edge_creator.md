# Documentação do Agente `edge_creator`

## Propósito
O agente `edge_creator` é responsável por criar as conexões (edges) entre os nodes dentro do framework Dify. Ele processa a arquitetura do sistema e adiciona as edges ao arquivo YAML correspondente.

## Funcionalidade
O agente `edge_creator` tem como principal função criar e organizar as conexões entre os nodes do dify, utilizando as ferramentas disponíveis no Dify. Ele segue os seguintes passos:

1. **Recebe o estado atual (`DifyState`)**
    - Contém informações sobre os nodes e edges a serem criadas.
    - Inclui mensagens acumuladas no fluxo de execução.
2. **Invoca o modelo `edge_creator_dify_model`**
    - Processa os dados da arquitetura.
    - Gera a resposta com as edges adequadas.
3. **Atualiza o estado e retorna um comando**
    - Atualiza a lista de mensagens com a resposta gerada.
    - Define `goto="__end__"`, indicando o encerramento do processo.

## Criação de Edges
O agente pode criar conexões entre os nodes utilizando a seguinte ferramenta:
- **Create Edge**: Criado com `create_edges(id: str, source_id: str, target_id: str)`.

## Considerações Finais
O `edge_creator` trabalha em conjunto com o `node_creator`, garantindo que todos os nodes gerados estejam devidamente conectados dentro do Dify. Ele é a etapa final na geração da infraestrutura do sistema.

