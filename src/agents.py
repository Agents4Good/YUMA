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

def assistent_agent(state: AgentState) -> Command[Literal["human_node", "architect_agent"]]:
    system_prompt = """
    You are an expert in multi-agent system architectures. 
    Your role is to help the user build a detailed description of the system from an initial idea. 
    Always refine the requirements with additional questions, ensuring that the system is well specified.

    Instructions:
    1. Always answer only in the user's language.
    2. If the user's initial description is incomplete, ask for more information, such as:
    - What problem does the system solve?
    - Who are the end users?
    - What should the system do?
    - What technologies can be used (languages, frameworks, architecture)?
    Explain to the user what is needed to answer these points.
    3. If the user is unable to talk about some information, suggest the detailed information that details the system flows and ask for the user's opinion at every step.
    4. Respond ONLY if the message is related to building multi-agent systems. Other topics will not be considered.

    5. When the user indicates that he/she has finished or accepted the suggested description, generate the final version of the document with:

    Expected user input:
    The user will provide an initial description containing:

    - Purpose of the system and main requirements:
    - What problem does the system solve?
    - Who are the end users?
    - What should the system do?
    - Preferred technologies: If applicable, mention frameworks, languages ​​or patterns.

    Expected output:
    Return the final description approved by the user, organized into topics.

    Submit feedback or jump to the end when the human approves the description.
    At the end of the interaction with the human, pass the collected information to "architect_agent" writing an "#architect_agent" code in the end.
    """
    messages = state["messages"] + [SystemMessage(content=system_prompt)]
    response = model.invoke(messages)
    
    messages.append(response)
    if "#architect_agent" in response.content:
        return Command(
            update={
                "messages" : messages,
                "active_agent" : "architect_agent"
            }, goto="human_node")
    return Command(
        update={
                "messages" : messages,
                "active_agent" : "assistent_agent"
            }, goto="human_node")

def architect_agent(state: AgentState) -> Command[Literal["human_node", "__end__"]]:
    system_prompt = """
    Instruction:
    You are a multi-agent system architect. Based on the user's input, design a multi-agent system that meets the user's needs. 
    You must return a description of the multi-agent system, including:
    - Agents: The roles of each agent in the system.
    - Communication: The communication protocol between agents.
    """
    
    messages = state["messages"] + [SystemMessage(content=system_prompt)]
    response = model.invoke(messages)
    
    messages.append(response)
    return Command(
        update={
                "messages" : messages,
                "active_agent" : "architect_agent"
            }, goto="human_node")

def human_node(state: AgentState) -> Command[Literal['assistent_agent', 'architect_agent']]:
    """A node for collecting user input."""
    user_input = interrupt("Avalie a resposta do agente: ")
    active_agent = state["active_agent"]
    
    return Command(
        update={
            "messages" : [HumanMessage(content=user_input)]
        },
        goto=active_agent
    )