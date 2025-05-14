from langchain_core.messages.base import BaseMessage
from utils.genia import write_log
import json
import re


def content_to_tool(message: BaseMessage):
    pattern = r"<function=(\w+)(\{.*?\})<\/function>"
    matches = re.findall(pattern, message.content)
    write_log("content_to_tool matches", matches)
    
    result = []

    for func_name, args_str in matches:
        write_log("content_to_tool func_name", func_name)
        write_log("content_to_tool args_str", args_str)
        try:
            args = json.loads(args_str)
        except json.JSONDecodeError:
            continue

        result.append({
            'name': func_name,
            'args': args,
            'type': 'tool_call'
        })
    message.tool_calls = result
    return message
