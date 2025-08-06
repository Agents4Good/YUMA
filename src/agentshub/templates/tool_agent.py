AGENT_TEMPLATE = '''
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from tools import {tool_name1}, {tools_name2}, {tool_name_n}
from dotenv import load_dotenv

load_dotenv(override=True)

model = ChatOpenAI(model="gpt-4o")

tools = [{tools}]
model_with_tools = model.bind_tools(tools)

def {agent_name}(state: MessagesState) -> MessagesState:
    prompt = SystemMessage(content="""{prompt}""")

    messages = state["messages"] + [prompt]

    return state["messages"].append(model_with_tools.invoke(messages))
'''

TOOL_TEMPLATE = '''
@tool
def {tool_name}({params}):
    """
    {description}
  
    Args:
    {params_doc}
  
    Returns:
    {return_doc}
    """
    {code}
'''

MAIN_TEMPLATE = """
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from {agent_folder} import {agent_name}, tools
from dotenv import load_dotenv

load_dotenv(override=True)


def edge_condicional(state: MessagesState) -> str:
    if state["messages"][-1].tool_calls:
        return "tools"

    return END


def build_graph():
    tool_node = ToolNode(tools)

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", {agent_name})
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", edge_condicional, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()


def execute_graph(input: str) -> str:
    initial_state = MessagesState(messages=[HumanMessage(input)])
    graph = build_graph()

    result = graph.invoke(initial_state)
    return result["messages"]


if __name__ == "__main__":
    messages = execute_graph(input("$ "))
    for message in messages:
        print(message)
        if isinstance(message, AIMessage) and message.tool_calls:
            print("Tool Call:", message.tool_calls)
"""