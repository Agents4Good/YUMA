
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


def build_few_shot(architecture: str, original_prompt: str, examples: List[BaseMessage], node_type: str) -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", original_prompt + "\nEXEMPLOS\n"),
            *examples,
        ]
    )

    prompt = SystemMessage(prompt_template.format())
    human_message = HumanMessage(
        f"A partir dos exemplos acima, construa os nós de {node_type} indicados nessa arquitetura:\n {architecture}")
    return [prompt] + [human_message]
