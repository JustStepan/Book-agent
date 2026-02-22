import json
from typing import Any, List


def msg_convertor(messgs: List[Any]) -> List[dict]:
    def lgch_to_openai_roles(tp: str) -> str:
        mapping = {
            "human": "user",
            "ai": "assistant",
            "tool": "tool"
        }
        return mapping[tp]
    
    messages = []
    for msg in messgs:

        new_message = {
            "role": lgch_to_openai_roles(msg.type),
            "content": msg.content,
        }

        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            new_message["tool_calls"] = []
            for tc in msg.tool_calls:
                new_message["tool_calls"].append({
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc["args"])
                    }
                })

        if hasattr(msg, 'tool_call_id'):
            new_message["name"] = msg.name
            new_message["tool_call_id"] = msg.tool_call_id
        
        messages.append(new_message)

    return messages