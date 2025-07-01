from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage
from agentshub.yuma.architect import ArchitectureOutput, Node, Interaction


def _architecture_example():
    nodes = [Node(node="start_node", description="Nó de entrada do usuário, vai ser mapeado para (Start Node) do dify"),
             Node(node="cep_extracao", description="Nó de extração do CEP, vai ser mapeado para (LLM Node) do dify"),
             Node(node="cep_pesquisa", description="Nó de pesquisa do CEP, vai ser mapeado para (HTTP Request Node) do dify"),
             Node(node="cep_resposta", description="Nó de resposta final, vai ser mapeado para (Answer Node) do dify")]
    
    interactions = [Interaction(source="start_node", target="cep_extracao", description="Recebimento da entrada do usuário e envio para extração do CEP"),
                    Interaction(source="cep_extracao", target="cep_pesquisa", description="Recebimento do CEP extraído e envio para pesquisa"),
                    Interaction(source="cep_pesquisa", target="cep_resposta", description="Recebimento do resultado da pesquisa e envio para resposta final")]
    
    return ArchitectureOutput(nodes=nodes, interactions=interactions, route_next=True).model_dump_json()

EXAMPLES = [
    HumanMessage(name="human_example", content='construa os nós de HTTP indicados nessa arquitetura:\n ' + _architecture_example()),
    AIMessage(name="desenvolvedor_exemplo",
              content="tools_calls=[" +
              "{'name': 'create_llm_node', " +
                   "'args': " +
                   "{'title': 'Piada Gerador', " +
              "'node_id': 'piada_gerador', " +
              "'role': 'Você é um especialista em contar piadas', " +
              "'context_variable': 'sys.query', " +
              "'task': 'Gere piadas curtas e simples', " +
              "'temperature': 0.5}, " +
                   "'id': '1'}]")
]
