from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage

EXAMPLES = [
    HumanMessage(name="human_example", content='construa os nós de LLM indicados nessa arquitetura:\n {"nodes":[' +
                 '{"node":"start_node","description":"Nó inicial que fornece informações essenciais para o sistema, mapeado para (Start Node) do dify"},' +
                 '{"node":"piada_geradora","description":"Gera piadas completamente aleatórias e improvisadas, sem uma base de conhecimento pré-existente, mapeado para (LLM Node) do dify"},' +
                 '{"node":"resposta_final","description":"Fornece a piada gerada como resposta final, mapeado para (Answer Node) do dify"}],' +
                 '"interactions":[' +
                 '{"source":"start_node","targets":"piada_geradora","description":"Envio de informações iniciais para geração de piada"},' +
                 '{"source":"piada_geradora","targets":"resposta_final","description":"Envio da piada gerada para resposta final"}],"route_next":true}'),
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
