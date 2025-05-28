from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage
from agentshub.genia.architect import ArchitectureOutput, Node, Interaction

def _architecture_example():
    nodes = [Node(node="start_node", description="Nó inicial que fornece informações essenciais para o sistema, mapeado para (Start Node) do dify"),
             Node(node="atualizador_de_noticias", description="Nó responsável por buscar novas notícias de um assunto, com uma tool, e retornar um resumo delas, mapeado para (Agent Node) do Dify"),
             Node(node="resposta_final", description="Fornece os resumos das notícias buscadas como resposta final, mapeado para (Answer Node) do dify")]

    interactions = [Interaction(source="start_node", target="atualizador_de_noticias", description="Envio de informações iniciais para busca de notícias"),
                    Interaction(source="atualizador_de_noticias", target="resposta_final", description="Envio dos resumo das notícias para resposta final")]

    return ArchitectureOutput(nodes=nodes, interactions=interactions, route_next=True).model_dump_json()

EXAMPLES = [
    HumanMessage(name="human_example", content='construa os nós de AGENTE indicados nessa arquitetura:\n ' + _architecture_example()),
    AIMessage(name="desenvolvedor_exemplo",
              content="tools_calls=[" +
              "{'name': 'create_agent_node', " +
                   "'args': " +
                   "{'title': 'Atualizador de Notícias', " +
              "'node_id': 'atualizador_de_noticias', " +
              "'instruction': 'Voce é um especialista em me atualizar sobre as noticias da guerra na ucrania.\n\nFaça uma pesquisa na web sobre o assunto\n\nUse a ferramenta disponivel para pegar as atualizações mais recentes. Pesquise por exemplo 'Novidades da guerra da ucrania'. Coloque ao lado da noticia o link da fonte', " +
              "'context_variable': 'sys.query', " +
              "'tool': [tavily_search], " +
              "'temperature': 0.5}, " +
                   "'id': '1'}]")
]
