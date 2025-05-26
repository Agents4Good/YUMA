from langchain_core.messages import AIMessage
from langchain_core.messages.base import BaseMessage
import json
import re
import uuid

def content_to_tool(message: BaseMessage):
    pattern = r"<function=([a-zA-Z_][a-zA-Z0-9_])>\s(\{.?\})(?:\s;)?"
    matches = re.findall(pattern, message.content)
    print(matches)
    result = []

    for func_name, args_str in matches:
        print("===============func_name\n", func_name)
        print("===============args_str\n", args_str)

        print("================")
        try:
            args = json.loads(args_str)
        except json.JSONDecodeError:
            continue

        result.append({
            'name': func_name,
            'args': args,
            'id': str(uuid.uuid4()),
            'type': 'tool_call'
        })
    message.tool_calls = result
    return message
