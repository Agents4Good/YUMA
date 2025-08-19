CONVERSATIONAL_AGENT_TEMPLATE = '''
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph
import os
import sys

api_key = os.getenv("OPENAI_API_KEY")

# Inicialização do modelo
model = ChatOpenAI(model="gpt-4o")

# Prompt do agente
def {agent_name}(state: MessagesState) -> MessagesState:
    prompt = SystemMessage(content={prompt})
    
    messages = [prompt] + state["messages"]
    response = model.invoke(messages)
    
    return MessagesState(messages=messages + [response])

# Função para construir o grafo simples sem ferramentas
def build_graph():
    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", {agent_name})
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()

# Função de execução do grafo
def execute_graph(input: str) -> str:
    initial_state = MessagesState(messages=[HumanMessage(content=input)])
    graph = build_graph()
    result = graph.invoke(initial_state)
    return result["messages"]

# Execução direta (modo script)
if __name__ == "__main__":
    messages = execute_graph(input("Você: "))
    for message in messages:
        print(f"{message.type.capitalize()}: {message.content}")
'''
