
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


def build_few_shot(original_prompt: str, examples: List[BaseMessage], human_message: HumanMessage = None) -> str:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", original_prompt + "\nEXEMPLOS\n"),
            *examples,
        ]
    )

    prompt = SystemMessage(prompt_template.format())
    if not human_message:
        return [prompt]
    
    return [prompt] + [human_message]
