from state import AgentState
from tools import make_handoff_tool

from langgraph.types import Command, interrupt
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from typing import Literal

from dotenv import load_dotenv

import os

load_dotenv(override=True)
model = ChatOpenAI(model="gpt-4-turbo")

def assistent_agent(state: AgentState) -> Command[Literal["human_node", "__end__"]]:
    system_prompt = """
    You are a useful assistant. Transfer to end when the human says that he finish the conversation.
    """
    messages = state["messages"] + [SystemMessage(content=system_prompt)]
    response = model.invoke(messages)
    
    messages.append(response)
    return Command(
        update={
                "messages" : messages,
                "active_agent" : "assistent_agent"
            }, goto="human_node")

def human_node(state: AgentState) -> Command[Literal['requirements_analyzer_agent','__end__']]:
    """A node for collecting user input."""
    user_input = interrupt("Avalie a resposta do agente: ")
    active_agent = state["active_agent"]
    
    return Command(
        update={
            "messages" : [HumanMessage(content=user_input)]
        },
        goto=active_agent
    )

def requirements_analyzer_agent(state: AgentState) -> Command[Literal["human_node", "__end__"]]:
    system_prompt = """
    You are a requirements analysis assistant specialized in multi-agent systems.
    Your goal is to ensure that the human provides all the necessary details before proceeding.
    
    A multi-agent system should have at least:
    - A clear system objective
    - Main agents and their responsibilities
    - Communication protocols between agents(optional)
    - Decision-making mechanisms (centralized or decentralized)
    - Environment interactions (how agents perceive and act)
    
    If any of these details are missing, ask the human to provide them.
    Once all requirements are met, inform the human that they are sufficient.
    """
    messages = state["messages"] + [SystemMessage(content=system_prompt)]
    response = model.invoke(messages)
    
    messages.append(response)
    return Command(
        update={
                "messages" : messages,
                "active_agent" : "requirements_analyzer_agent"
            }, goto="human_node")