# Gerador de Aplicações

## Visão Geral

O sistema é baseado em uma **arquitetura multiagente**, onde diferentes agentes desempenham papéis específicos para alcançar objetivos comuns. A arquitetura é projetada para ser:

- **Modular** - permite a composição flexível de componentes
- **Escalável** - possibilita a adição de novos agentes conforme necessário

## Componentes do Sistema

| Agente                | Responsabilidade                                                                 |
|-----------------------|----------------------------------------------------------------------------------|
| Requirements Engineer | Especialista em arquiteturas de sistemas multiagentes, guia a definição do sistema |
| Architecture Agent    | Recebe a descrição do sistema e cria a arquitetura solicitada                    |
| Supervisor Agent      | Coordena a criação de nós e arestas no framework Dify                           |
| Node Creator          | Desenvolvedor que preenche o arquivo YAML com os nós para representar os agentes |
| Edge Creator          | Responsável por criar as conexões (arestas) entre os nós                        |

## Fluxo de Trabalho

1. **Início**  
   → O `requirements_engineer` coleta informações e refina a especificação do sistema

2. **Criação de Arquitetura**  
   → O `architecture_agent` recebe a especificação e gera a arquitetura

3. **Supervisão e Criação**  
   → O `supervisor_agent` coordena:  
     - `node_creator`: cria nós  
     - `edge_creator`: estabelece conexões  

4. **Integração com Dify**  
   → A arquitetura é implementada no framework usando:  
     - **Nós**: representam agentes  
     - **Arestas**: representam interações  

## Tecnologias Utilizadas

- **Framework Dify**  
  Plataforma para criação/gerenciamento de grafos de agentes

- **LLMs (Large Language Models)**  
  Modelos de linguagem para geração de componentes específicos

## Diagrama de Interação

```mermaid
graph TD
    A[Requirements Engineer] --> B[Architecture Agent]
    B --> C[Supervisor Agent]
    C --> D[Node Creator]
    C --> E[Edge Creator]
    D --> F[Framework Dify]
    E --> F