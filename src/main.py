from state import AgentState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from agents import requirements_analyser_agent, assistent_agent, human_node
import uuid
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

def build_graph():
    builder = StateGraph(AgentState)

    #Nodes
    builder.add_node("requirements_analyser_agent", requirements_analyser_agent)
    builder.add_node("assistent_agent", assistent_agent)
    builder.add_node("human_node", human_node)
    
    #Edges
    builder.add_edge(START, "requirements_analyzer_agent")
    builder.add_edge("requirements_analyzer_agent", "human_node")
    builder.add_edge("human_node", "requirements_analyzer_agent")  # Loop até que os requisitos mínimos sejam atendidos
    builder.add_edge("requirements_analyzer_agent", "assistent_agent")  # Continua para o assistente quando pronto
    builder.add_edge("assistent_agent", "human_node")
    
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)

    
def main():
    graph = build_graph()
    thread_config = {"configurable": {"thread_id": uuid.uuid4()}}
    human_message = input("Digite sua entrada: ")
    user_input = AgentState(messages=HumanMessage(content=human_message))
    num_conversation = 0
    while True:
        print()
        print(f"--- Conversation Turn {num_conversation} ---")
        print()
        if not num_conversation == 0:
            human_message = input(f"User: ")
            user_input = Command(resume=human_message)
        print()
        for update in graph.stream(
            user_input,
            config=thread_config,
            stream_mode="updates",
        ):
            for node_id, value in update.items():
                if isinstance(value, dict) and value.get("messages", []):
                    last_message = value["messages"][-1]
                    if isinstance(last_message, dict) or last_message.type != "ai":
                        continue
                    print(f"{node_id}: {last_message.content}")
        num_conversation =+ 1


if __name__ == "__main__":
    main()