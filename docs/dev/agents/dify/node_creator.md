# Documentação do Agente `node_creator`

## Propósito
O agente `node_creator` é responsável por gerar os nodes necessários para representar os agentes do sistema dentro do framework Dify. Ele processa a arquitetura gerada e preenche o arquivo YAML correspondente.

## Funcionalidade
O agente tem como principal função a criação e organização dos nodes no arquivo YAML, utilizando as ferramentas disponíveis no Dify. Ele segue os seguintes passos:

1. **Recebe o estado atual (`DifyState`)**
    - Contém informações sobre os nodes a serem criados.
    - Inclui mensagens acumuladas no fluxo de execução.
2. **Adiciona o prompt do sistema (`NODE_CREATOR`)**
    - Define a função principal do agente dentro do fluxo Dify.
3. **Invoca o modelo `node_creator_dify_model`**
    - Processa os dados da arquitetura.
    - Gera a resposta com os nodes adequados.
4. **Atualiza o estado e retorna um comando**
    - Atualiza a lista de mensagens com a resposta gerada.
    - Encaminha para `edge_creator`, que será responsável por criar as conexões entre os nodes.

## Tipos de Nodes Criados
O agente pode criar os seguintes tipos de nodes dentro do Dify:

- **LLM Node**: Criado com `create_llm_node(id: str, title: str, prompt: str)`.
- **Answer Node**: Criado com `create_answer_node(title: str, id: str, answer: str)`.
- **Start Node**: Criado com `create_start_node(title: str, id: str)`.

## Considerações Finais
O `node_creator` desempenha um papel essencial na estruturação dos agentes dentro do Dify, convertendo a arquitetura em uma representação funcional no YAML. Ele trabalha em conjunto com `edge_creator`, que se encarrega das conexões entre os nodes.

