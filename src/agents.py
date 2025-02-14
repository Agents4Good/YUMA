from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os

load_dotenv(override=True)
model = ChatOpenAI(model="gpt-4-turbo")

def assistent_agent(state: MessagesState) -> MessagesState:
    system_prompt = """
    You are a useful assistant
    """
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)

    state["messages"].append(response)
    return state