from langgraph.graph import MessagesState,  StateGraph, START, END
from langchain_core.messages import HumanMessage
from agents import assistent_agent


def build_graph():
    builder = StateGraph(MessagesState)

    builder.add_node("assistent_agent", assistent_agent)

    builder.add_edge(START, "assistent_agent")
    builder.add_edge("assistent_agent", END)

    return builder.compile()

    
def main():
    graph = build_graph()
    human_message = input("Digite sua entrada: ")
    initial_state = MessagesState(messages=[HumanMessage(content=human_message)])
    result = graph.invoke(initial_state)
    print(result)


if __name__ == "__main__":
    main()