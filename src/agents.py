from state import AgentState
from tools import make_handoff_tool
from outputs import ArchitectureOutput

from langgraph.prebuilt import create_react_agent
from langgraph.types import Command, interrupt
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from typing import Literal

from dotenv import load_dotenv

import os

load_dotenv(override=True)

architecture_tool = [make_handoff_tool(agent_name="architecture_agent")]
end_tool = [make_handoff_tool(agent_name="__end__")]

model = ChatOpenAI(model="gpt-4o-mini")
architecture_model = model.with_structured_output(ArchitectureOutput)

def assistent_agent(state: AgentState) -> Command[Literal["human_node", "architecture_agent"]]:
    system_prompt = """
    You are an expert in multi-agent system architectures. When the user provides a system description, generate a structured architecture outlining agents, interactions, and execution flow. 
    Transfer to end when the human says that they have finished the conversation.
    
    Instruction:
    You are a specialist in multi-agent system architectures. Based on the user's input, generate a detailed architecture.
    RESPONSE ONLY IN LANGUAGE OF USER. 
    ONLY!!!! reply if the message is related to the generation of multi-agent systems. Other topics will not be considered.

    Input:
    The user will provide a description including:
    - System Goal: What the system should solve or optimize.
    - Types of Agents: If known, describe their roles.
    - Agent Interactions: How they communicate and collaborate.
    - Environment: Where the system operates and any constraints.
    - Preferred Technologies: If applicable, mention frameworks, languages, or standards.

    
    Expected Output:
    You must return an architecture that includes:
    1. List of Agents and their responsibilities.
    2. Communication Model (e.g., direct messaging, event-driven, blackboard system).
    3. Execution Flow explaining how agents collaborate to achieve the goal.
    4. Suggested Structural Diagram (e.g., UML, Entity-Relationship, Event Flow).
    5. Recommended Technologies, including:
    - Multi-agent frameworks (e.g., LangGraph, JADE, SPADE, OpenAI Autonode).
    - Models of LLM (e.g., ChatGPT, Gemini, Llama)

    If any information is unclear, ask the user for clarification before finalizing the architecture.
    If the human is satisfied with the system description, then ask for help to the "architecture_agent".
    """
    assistent_model = create_react_agent(
        model,
        tools=architecture_tool,
        prompt=system_prompt
    )
    response = assistent_model.invoke(state)
    response['active_agent'] = 'assistent_agent'
    return Command(
        update=response, goto="human_node")

# Errado, não está gerando o structured output
def architecture_agent(state: AgentState) -> Command[Literal["human_node", "__end__"]]:
    system_prompt = """
    You are an expert in multi-agent system architectures. Your goal is to receive a system description and create the architecture of the system asked, using the structured output.
    When the human is satisfied with your answer, 'route_next' must be true. Otherwise, 'route_next' must be false
    """
    messages = state["messages"] + [SystemMessage(content=system_prompt)]
    
    response = architecture_model.invoke(messages)
    
    goto = 'human_node'
    if response.route_next:
        goto = '__end__'
    
    return Command(
        update={
            "messages": messages,
            "active_agent": "architect_agent",
            "architecture_output": response
        }, 
        goto=goto)


def human_node(state: AgentState) -> Command[Literal['assistent_agent','architecture_agent']]:
    """A node for collecting user input."""
    user_input = interrupt("Avalie a resposta do agente: ")
    active_agent = state["active_agent"]
    
    return Command(
        update={
            "messages" : [HumanMessage(content=user_input)]
        },
        goto=active_agent
    )