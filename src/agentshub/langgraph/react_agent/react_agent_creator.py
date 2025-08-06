from langchain_core.messages import SystemMessage
from schema.langgraph import LangState
from .tools import criar_agente_react, criar_tool, criar_documentacao
from models import model_sys
from .prompt import REACT_AGENT_CREATOR


react_agent_creator_tools = [criar_agente_react, criar_tool, criar_documentacao]
model_with_tools = model_sys.bind_tools(react_agent_creator_tools)

def react_agent_creator(state: LangState) -> LangState:
    print(state["messages"][-1])
    prompt = SystemMessage(content=REACT_AGENT_CREATOR)
    messages = state["messages"] + [prompt]
    response = model_with_tools.invoke(messages)
    print("-=-=-=-="*30)
    print(response)
    return {"messages" : [response]}