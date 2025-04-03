# Documentação do Agente `architecture_agent`

## Propósito
O agente `architecture_agent` é responsável por processar os requisitos definidos pelo agente `requirements_engineer` e transformar essas informações em uma estrutura arquitetural coerente para um sistema multiagente.

## Implementação
A função `architecture_agent` é definida da seguinte forma:

```python
def architecture_agent(state: AgentState) -> Command[Literal["human_node", "dify"]]:
    system_prompt = agents_prompts.ARCHITECTURE_AGENT
    buffer = state.get("buffer", [])
    if not buffer:
        filtered_messages = [
            msg
            for msg in state["messages"]
            if isinstance(msg, AIMessage) and msg.content.strip() != ""
        ]

        last_ai_message = next(
            (msg for msg in reversed(filtered_messages) if isinstance(msg, AIMessage)),
            None,
        )

        buffer = [last_ai_message] + [SystemMessage(content=system_prompt)]

    response = architecture_model.invoke(buffer)
    goto = "human_node"
    if response.route_next:
        goto = "dify"

    sequence_diagram_generator.invoke(response.model_dump_json())

    buffer.append(AIMessage(content=response.model_dump_json()))

    return Command(
        update={
            "messages": state["messages"],
            "active_agent": "architecture_agent",
            "architecture_output": response,
            "buffer": buffer,
        },
        goto=goto,
    )
```

## Prompt `ARCHITECTURE_AGENT`

```python
ARCHITECTURE_AGENT = """
    Você é um especialista em arquiteturas de sistemas multiagentes. 
    Seu objetivo é receber uma descrição do sistema e criar a arquitetura do sistema solicitado, usando a saída estruturada.

    IMPORTANTE:
    - Ignore quaisquer mensagens anteriores que indiquem satisfação com as respostas de outros agentes.
    - Avalie a satisfação humana somente com base no feedback que aborda explicitamente sua saída.

    Quando você determinar que o humano está satisfeito com sua proposta arquitetônica, defina 'route_next' como true;
    caso contrário, defina 'route_next' como false.
"""
```

## Saída `ArchitectureOutput`

```python
class ArchitectureOutput(BaseModel):
    """
    Represents the architecture of the multi-agent system.
    """
    agents: List[Agent] = Field(description="List of agents in the multi-agent system")
    interactions: List[Interaction] = Field(description="List of interactions between agents, "
                                                            "where each interaction has a source agent and a target agent")
    route_next: bool = Field(default_factory=lambda: False, description="Determines if the graph should proceed to the next node (True) or remain in the current node (False).")
```

## Funcionalidade
O agente utiliza um modelo de arquitetura (`architecture_model`) para processar a entrada e gerar uma saída estruturada. Ele também utiliza `sequence_diagram_generator` para gerar diagramas baseados na saída do modelo.

1. **Recebe o estado do agente (`state`)**: Contendo informações sobre a interação atual.
2. **Verifica o buffer de mensagens**:
    - Se o buffer estiver vazio, filtra mensagens anteriores do agente AI.
    - Recupera a última mensagem relevante do agente AI.
    - Adiciona uma mensagem do sistema com o prompt `ARCHITECTURE_AGENT`.
3. **Invoca o modelo `architecture_model`**:
    - Processa as mensagens do buffer.
    - Gera uma resposta estruturada.
4. **Determina o próximo destino (`goto`)**:
    - Padrão: `human_node`.
    - Caso `response.route_next` esteja definido, direciona para `dify`.
5. **Gera um diagrama de sequência**:
    - Utiliza `sequence_diagram_generator` para criar um diagrama baseado na resposta.
6. **Atualiza o buffer**:
    - Adiciona a resposta do modelo ao buffer.
7. **Retorna um comando**:
    - Atualiza o estado com as mensagens e a saída do agente.
    - Define `active_agent` como `architecture_agent`.
    - Encaminha para o próximo nó (`human_node` ou `dify`).

## Considerações Finais
O `architecture_agent` é projetado para estruturar a arquitetura do sistema com base nos requisitos previamente definidos. Ele também gera diagramas de sequência para visualizar a interação entre os componentes do sistema.

