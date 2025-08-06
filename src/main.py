from schema.yuma import AgentState
from schema.dify import DifyState
from agentshub.yuma import (
    requirements_engineer,
    architect,
    human_node,
)
from agentshub.yuma.gemini_cli import gemini_cli
from agentshub.dify import (
    supervisor,
    start_node_creator,
    llm_node_creator,
    http_node_creator,
    logic_node_creator,
    answer_node_creator,
    agent_node_creator,
    edge_creator,
    yaml_analyzer,
    extractor_document_node_creator
)

from utils.dify import dify_yaml_builder, call_dify_tools

from utils.yuma.print_functions import (
    print_conversation_header,
    print_node_header,
    print_break_line,
    get_pretty_input,
    print_architecture,
    write_log,
)

from utils.yuma.io_functions import print_graph

import uuid

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage


node_creation = [
    "start_node_creator",
    "llm_node_creator",
    "logic_node_creator",
    "http_node_creator",
    "agent_node_creator",
    "answer_node_creator",
    "extractor_document_node_creator",
]


def supervisor_conditional_edge(state: DifyState):
    agents = state["messages"][-1].content.split(", ")
    write_log("supervisor_conditional_edge", agents)
    return agents


def build_graph():
    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("requirements_engineer", requirements_engineer)
    builder.add_node("human_node", human_node)
    builder.add_node("architecture_agent", architect)
    builder.add_node("gemini_cli", gemini_cli)

    # Edges
    builder.add_edge(START, "requirements_engineer")

    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


def get_user_input(isInitial, num_conversation=0):
    if isInitial:
        print_conversation_header(num_conversation)

    human_message = get_pretty_input()
    print_break_line()

    if human_message.lower() == "q":
        return None

    return (
        AgentState(messages=[HumanMessage(content=human_message)])
        if isInitial
        else Command(resume=human_message)
    )


def handle_stream(graph, user_input, config):
    final_state = None
    for update in graph.stream(user_input, config=config, stream_mode="updates"):
        for node_id, value in update.items():
            if isinstance(value, dict) and value.get("messages", []):
                last_message = value["messages"][-1]
                if not isinstance(last_message, dict) and last_message.type == "ai":
                    print_node_header(node_id, last_message.content)
                final_state = value
    return final_state


def main():
    graph = build_graph()
    # print_graph(graph)
    thread_config = {"configurable": {"thread_id": uuid.uuid4()}}
    num_conversation = 0
    user_input = get_user_input(True, num_conversation)

    while user_input != None:
        print("main")
        num_conversation += 1
        final_state = handle_stream(graph, user_input, config=thread_config)
        print_conversation_header(num_conversation)

        architecture_output = final_state.get("architecture_output") if final_state else None
        # if architecture_output and final_state.get("active_agent") == "architecture_agent":
        #     print_architecture(architecture_output)

        user_input = get_user_input(False)


if __name__ == "__main__":
    main()
