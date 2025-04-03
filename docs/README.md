# 📚 Documentação do Sistema Multiagente

Bem-vindo à documentação do sistema multiagente! Aqui você encontrará informações detalhadas sobre a arquitetura, especificação e implementação dos agentes que compõem o sistema.

## 📂 Estrutura da Documentação

A documentação está organizada da seguinte forma:

### 📌 `dev/`

- **`agents/`** – Documentação dos agentes do sistema.
  - `dify/` – Agentes relacionados ao framework Dify.
    - `edge_creator.md` – Responsável por criar conexões entre os agentes.
    - `node_creator.md` – Responsável por criar os nós do sistema.
    - `supervisor.md` – Gerencia a criação dos nós e conexões.
  - `architecture.md` – Estrutura da arquitetura dos agentes.
  - `requirements_engineer.md` – Define os requisitos do sistema.

- **`tools/`** – Ferramentas utilizadas no sistema.
  - `make_handoff.md` – Responsável por repassar o controle entre agentes.
  - `sequence_diagram_generator.md` – Gera diagramas de sequência para visualização da arquitetura.
  - `dify/` – Ferramentas do framework Dify.
    - `create_answer_node.md` – Cria nós de resposta.
    - `create_edges.md` – Cria conexões entre os agentes.
    - `create_llm_node.md` – Cria nós de modelo de linguagem.
    - `create_metadata.md` – Define metadados para o sistema.
    - `create_start_node.md` – Cria nós iniciais do fluxo.
    

- **`workflow/`** – Explica o fluxo de funcionamento do sistema.

### 📖 Outros Documentos
- **`arquitetura.md`** – Detalhes sobre a arquitetura geral do sistema.
- **`guias/`** – Exemplos e guias práticos.

## 🚀 Como Usar
1. Consulte `arquitetura.md` para entender a estrutura geral do sistema.
2. Veja `dev/agents/` para informações sobre os agentes do sistema.
3. Explore `guias/` para exemplos práticos de uso.