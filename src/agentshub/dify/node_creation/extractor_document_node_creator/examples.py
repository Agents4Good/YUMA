from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage
from agentshub.yuma.architect import ArchitectureOutput, Node, Interaction


def _extractor_example():
    nodes = [
        Node(node="start_extracao", description="Nó inicial do fluxo, responsável por capturar a entrada do usuário"),
        Node(node="extrair_documento", description="Nó responsável por extrair informações específicas do documento"),
        Node(node="resposta_final", description="Nó de resposta final com os dados extraídos"),
    ]

    interactions = [
        Interaction(source="start_extracao", target="extrair_documento", description="Recebe a entrada e envia para extração"),
        Interaction(source="extrair_documento", target="resposta_final", description="Recebe os dados extraídos e envia para resposta final")
    ]

    return ArchitectureOutput(nodes=nodes, interactions=interactions, route_next=True).model_dump_json()


EXAMPLES = [
    HumanMessage(
        name="human_example",
        content='A partir dos exemplos, construa os nós de EXTRAÇÃO DE DOCUMENTOS indicados nessa arquitetura\n' + _extractor_example()
    ),
    AIMessage(
        name="desenvolvedor_exemplo",
        content="tools_calls=[" +
                "{'name': 'create_extractor_document_node', " +
                "'args': " +
                "{'title': 'Entrada do Usuário', " +
                "'node_id': 'start_extracao'}, " +
                "'id': '1'}]"
    )
]
