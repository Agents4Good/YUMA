from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"input":
        '{"nodes":[' +
     '{"node":"start_node","description":"Nó inicial que fornece informações essenciais para o sistema, mapeado para (Start Node) do dify"},' +
     '{"node":"piada_geradora","description":"Gera piadas completamente aleatórias e improvisadas, sem uma base de conhecimento pré-existente, mapeado para (LLM Node) do dify"},' +
     '{"node":"resposta_final","description":"Fornece a piada gerada como resposta final, mapeado para (Answer Node) do dify"}],' +
        '"interactions":[' +
     '{"source":"start_node","targets":"piada_geradora","description":"Envio de informações iniciais para geração de piada"},' +
     '{"source":"piada_geradora","targets":"resposta_final","description":"Envio da piada gerada para resposta final"}],"route_next":true}',
     "output":
        "tool_calls=[{'name': 'transfer_to_architecture_agent', 'id': '1']"
     }
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("ai", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)


if __name__ == "__main__":
    print(few_shot_prompt.invoke({}).to_messages())
