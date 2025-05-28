from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage
from agentshub.genia.architect import ArchitectureOutput, Node, Interaction


def _architecture_example():
    nodes = [Node(node="inicio_conversa", description="Recebe a entrada do usuário, tipo de nó: Start Node"),
             Node(node="gerador_de_piadas", description="Gera piadas para o usuário, tipo de nó: LLM Node"),
             Node(node="verificador_de_feedback", description="Verifica se o usuário gostou da piada, tipo de nó: If/Else Node"),
             Node(node="resposta_positiva", description="Envia uma resposta positiva ao usuário, tipo de nó: Answer Node"),
             Node(node="resposta_negativa", description="Envia uma resposta negativa ao usuário e solicita mais uma piada, tipo de nó: Answer Node")]

    interactions = [Interaction(source="inicio_conversa", target="gerador_de_piadas", description="Envia a entrada do usuário para gerar uma piada"),
                    Interaction(source="gerador_de_piadas", target="verificador_de_feedback", description="Envia a piada gerada para verificar o feedback do usuário"),
                    Interaction(source="verificador_de_feedback", target="resposta_positiva", description="Caso o usuário tenha gostado da piada"),
                    Interaction(source="verificador_de_feedback", target="resposta_negativa", description="Caso o usuário não tenha gostado da piada")]

    return ArchitectureOutput(nodes=nodes, interactions=interactions, route_next=True).model_dump_json()

EXAMPLES = [
    HumanMessage(name="human_example", content='construa os nós de LÓGICA indicados nessa arquitetura:\n ' + _architecture_example()),
    AIMessage(name="desenvolvedor_exemplo",
              content="tools_calls=[" +
              "{'name': 'create_contains_logic_node', " +
               "'args': " +
                   "{'title': 'Verificador de Feedback', " +
                    "'value': 'aprovado', " +
                    "'context_variable': 'sys.query', " +
                    "'id': '1'}]")
]
