# Graph Builder Module

## Visão Geral
O arquivo 'main.py' é o Módulo principal que constrói e executa o grafo de agentes para geração de aplicações. Implementa um fluxo de trabalho multiagente usando LangGraph e permite a interação com o humano.

#### Fluxos de execução
##### Fluxo Principal

```mermaid
graph TD
    A[START] --> B[Requirements Engineer]
    B --> C[Human Node]
    C --> D[Architecture Agent]
    D --> E[Dify Subgraph]
    E --> F[END]
```

##### Fluxo Secundario do Dify

```mermaid
graph TD
    A[START] --> B[Supervisor Agent]
    B --> C[Node Creator]
    C --> D[Tool Node Creator]
    D --> E[Edge Creator]
    E --> F[Tool Edge Creator]
    F --> G[END]
```
