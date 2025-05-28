from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage
from agentshub.yuma.architect import ArchitectureOutput, Node, Interaction


def _architecture_example():
    nodes = [Node(node="start_node", description="Nó inicial que fornece informações essenciais para o sistema, mapeado para (Start Node) do dify"),
             Node(node="piada_geradora", description="Gera piadas completamente aleatórias e improvisadas, sem uma base de conhecimento pré-existente, mapeado para (LLM Node) do dify"),
             Node(node="resposta_final", description="Fornece a piada gerada como resposta final, mapeado para (Answer Node) do dify")]

    interactions = [Interaction(source="start_node", target="piada_geradora", description="Envio de informações iniciais para geração de piada"),
                    Interaction(source="piada_geradora", target="resposta_final", description="Envio da piada gerada para resposta final")]

    return ArchitectureOutput(nodes=nodes, interactions=interactions, route_next=True).model_dump_json()

EXAMPLES = [
    HumanMessage(name="human_example", content='construa os nós de LLM indicados nessa arquitetura:\n ' + _architecture_example()),
    AIMessage(name="desenvolvedor_exemplo",
              content="tools_calls=[" +
              "{'name': 'create_llm_node', " +
                   "'args': " +
                   "{'title': 'Piada Geradora', " +
              "'node_id': 'piada_geradora', " +
              "'role': 'Você é um especialista em contar piadas', " +
              "'context_variable': 'sys.query', " +
              "'task': 'Gere piadas curtas e simples', " +
              "'temperature': 0.5}, " +
                   "'id': '1'}]")
]
