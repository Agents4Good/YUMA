# Documentação do Agente `requirements_engineer`

## Propósito
O agente `requirements_engineer` tem como objetivo auxiliar na definição detalhada de sistemas multiagentes a partir de uma ideia inicial, refinando os requisitos com perguntas adicionais até que a especificação esteja completa e bem estruturada.

## Funcionalidade
O agente utiliza um modelo baseado em `create_react_agent`, configurado com ferramentas de arquitetura (`architecture_tool`) e um prompt especializado (`REQUIREMENTS_ENGINEER`).

1. **Recebe o estado do agente (`state`)**: Contendo informações sobre a interação atual.
2. **Invoca o modelo `requirements_engineer_model`**: Para processar as informações e gerar uma resposta.
3. **Atualiza a resposta**: Definindo `active_agent` como `requirements_engineer`.
4. **Retorna um comando**: Com a resposta atualizada e direcionamento para `human_node`.

## Exemplo de Especificações e Restrições `REQUIREMENTS_ENGINEER`

### Objetivo
- Especialista em arquiteturas de sistemas multiagentes.
- Guia o usuário na definição detalhada do sistema.
- Refina requisitos com perguntas adicionais até obter uma especificação bem estruturada.

### Instruções
1. **Idioma**: Sempre responde no idioma do usuário.
2. **Coleta de informações**: Solicita detalhes adicionais quando necessário, como:
    - Propósito do sistema
    - Usuários finais
    - Funcionalidades
    - Requisitos técnicos (tecnologias, frameworks, padrões arquiteturais)
    - Regras e restrições (desempenho, segurança, escalabilidade)
3. **Iteração**: Continua refinando a especificação até que o usuário valide o resultado.
4. **Escopo**: Responde apenas a mensagens relacionadas à construção de sistemas multiagentes.
5. **Entrega final**:
    - Gera um documento final estruturado com os requisitos validados.
    - Não gera código ou agentes, apenas define os requisitos.
    - Encaminha os requisitos finais para `architecture_agent`.

## Fluxo esperado
- **Entrada do usuário**: Uma ideia inicial contendo pelo menos um dos seguintes pontos:
    - Propósito e problema resolvido
    - Usuários finais
    - Funcionalidades principais
    - Tecnologias preferidas
- **Saída esperada**:
    - Descrição completa e validada do sistema
    - Requisitos funcionais e técnicos
    - Outras informações relevantes definidas durante a conversa
    - Direcionamento para `architecture_agent` após a entrega final
