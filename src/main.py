from schema.yuma import AgentState
from schema.dify import DifyState
from agentshub.yuma import (
    requirements_engineer,
    architect,
    human_node,
)
from agentshub.dify import (
    supervisor,
    start_node_creator,
    llm_node_creator,
    http_node_creator,
    logic_node_creator,
    answer_node_creator,
    agent_node_creator,
    edge_creator,
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


dify_agents = [
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
    subgraph_builder = StateGraph(DifyState)

    subgraph_builder.add_node("supervisor_agent", supervisor)
    subgraph_builder.add_node("edge_creator", edge_creator)
    subgraph_builder.add_node("tools_node_creator", call_dify_tools)
    subgraph_builder.add_node("tools_edge_creator", call_dify_tools)
    subgraph_builder.add_node("dify_yaml_builder", dify_yaml_builder)
    subgraph_builder.add_node("start_node_creator", start_node_creator)
    subgraph_builder.add_node("llm_node_creator", llm_node_creator)
    subgraph_builder.add_node("logic_node_creator", logic_node_creator)
    subgraph_builder.add_node("http_node_creator", http_node_creator)
    subgraph_builder.add_node("agent_node_creator", agent_node_creator)
    subgraph_builder.add_node("answer_node_creator", answer_node_creator)
    subgraph_builder.add_node("extractor_document_node_creator", extractor_document_node_creator)

    dify_agents_map = {agent: agent for agent in dify_agents}
    subgraph_builder.add_edge(START, "supervisor_agent")
    subgraph_builder.add_conditional_edges(
        "supervisor_agent", supervisor_conditional_edge, dify_agents_map
    )
    subgraph_builder.add_edge("start_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("llm_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("logic_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("http_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("agent_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("answer_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("extractor_document_node_creator", "tools_node_creator")
    subgraph_builder.add_edge("tools_node_creator", "edge_creator")
    subgraph_builder.add_edge("edge_creator", "tools_edge_creator")
    subgraph_builder.add_edge("tools_edge_creator", "dify_yaml_builder")
    subgraph_builder.add_edge("dify_yaml_builder", END)
    subgraph = subgraph_builder.compile()

    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("requirements_engineer", requirements_engineer)
    builder.add_node("human_node", human_node)
    builder.add_node("architecture_agent", architect)
    builder.add_node("dify", subgraph)

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
        num_conversation += 1
        final_state = handle_stream(graph, user_input, config=thread_config)
        print_conversation_header(num_conversation)

        if final_state and (
            architecture_output := final_state.get("architecture_output")
        ):
            print_architecture(architecture_output)

        user_input = get_user_input(False)


if __name__ == "__main__":
    main()
