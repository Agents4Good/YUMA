# 📚 Documentação do Sistema Multiagente

Bem-vindo à documentação do sistema multiagente! Aqui você encontrará informações detalhadas sobre a arquitetura, especificação e implementação dos agentes que compõem o sistema.

## 📂 Estrutura da Documentação

A documentação está organizada da seguinte forma:

### 📌 `dev/`

- [**`agents/`**](./dev/agents/) – Documentação dos agentes do sistema.
  - [`dify/`](./dev/agents/dify/)– Agentes relacionados ao framework Dify.
    - [`edge_creator.md`](./dev/agents/dify/edge_creator.md) – Responsável por criar conexões entre os agentes.
    - [`node_creator.md`](./dev/agents/dify/node_creator.md) – Responsável por criar os nós do sistema.
    - [`supervisor.md`](./dev/agents/dify/supervisor.md) – Gerencia a criação dos nós e conexões.
  - [`architecture.md`](./dev/agents/architecture.md) – Estrutura da arquitetura dos agentes.
  - [`requirements_engineer.md`](./dev/agents/requirements_engineer.md) – Define os requisitos do sistema.

- [**`tools/`** ](./dev/tools/)– Ferramentas utilizadas no sistema.
  - [`make_handoff.md` ](./dev/tools/make_handoff.md)– Responsável por repassar o controle entre agentes.
  - [`sequence_diagram_generator.md`](./dev/tools/sequence_diagram_generator.md) – Gera diagramas de sequência para visualização da arquitetura.
  - [`dify/` ](./dev/tools/dify/)– Ferramentas do framework Dify.
    - [`create_answer_node.md`](./dev/tools/dify/create_answer_node.md) – Cria nós de resposta.
    - [`create_edges.md` ](./dev/tools/dify/create_edges.md)– Cria conexões entre os agentes.
    - [`create_llm_node.md` ](./dev/tools/dify/create_llm_node.md)– Cria nós de modelo de linguagem.
    - [`create_metadata.md`](./dev/tools/dify/create_metadata.md) – Define metadados para o sistema.
    - [`create_start_node.md` ](./dev/tools/dify/create_start_node.md)– Cria nós iniciais do fluxo.
    
- [**`workflow/`**](./dev/workflow/) – Explica o fluxo de funcionamento do sistema.

### 📖 Outros Documentos
- [**`arquitetura.md`** ](./dev/arquitetura.md)– Detalhes sobre a arquitetura geral do sistema.
- [**`guias/exemplos.md`** ](./guias/exemplos.md)– Exemplos e guias práticos.