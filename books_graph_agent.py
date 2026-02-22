import json
from typing import Any, List
import tools as tl
from openai import OpenAI
from prompts import PROMPTS
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from schema import BookAgentState

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="dummy-key",
)

MDLS = {
    'O': 'openai/gpt-oss-20b',
    'M': 'mistralai/devstral-small-2-2512',
    'DS': 'deepseek/deepseek-r1-0528-qwen3-8b',
    'L': 'liquid/lfm2.5-1.2b',
}

def _msg_convertor(messgs: List[Any]) -> List[dict]:
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


def llm_node(state: BookAgentState):
    messages = _msg_convertor(state['messages'])
    full_messages = [
        {"role": "system", "content": PROMPTS['query']['system']},
    ] + messages
    response = client.chat.completions.create(
        model=MDLS['O'],
        messages=full_messages,
        temperature=0.1,
        tools=tl.TOOLS_DESCRIPTION,
        tool_choice="auto",
    )
    message = response.choices[0].message
    if content := message.content:
        if "</think>" in content:
            content = content.split("</think>")[-1].strip()
        elif "<|constrain|>json<|message|>" in content:
            print('yes')
            content = content.split("<|constrain|>json<|message|>")[-1].strip()
            print(content)

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        id = tool_call.id

        return {'messages': [AIMessage(content=content or '', tool_calls=[{'name': function_name, 'args': arguments, "id": id}])]}

    return {'messages': [AIMessage(content=content)]}


def tool_node(state: BookAgentState):
    last_msg = state['messages'][-1]
    func_name = last_msg.tool_calls[0]['name']
    args = last_msg.tool_calls[0]['args']
    id = last_msg.tool_calls[0]['id']

    if hasattr(tl, func_name):
            
        func = getattr(tl, func_name)
        data = func(**args)
    else:
        raise ValueError(f"Tool '{func_name}' not found")

    if isinstance(data, str):
        data = json.dumps(data)

    return {'messages': [ToolMessage(content=str(data), tool_call_id=id, name=func_name)]}


def should_continue(state: BookAgentState):
    msg = state["messages"][-1]
    if not msg.tool_calls:
        return 'end'
    return 'tool'


def create_book_agent_graph():
    workflow = StateGraph(BookAgentState)

    workflow.add_node("llm", llm_node)
    workflow.add_node("tool", tool_node)

    workflow.set_entry_point("llm")
    workflow.add_edge("tool", "llm")

    workflow.add_conditional_edges(
        source="llm",
        path=should_continue,
        path_map={"tool": "tool", "end": END},
    )

    return workflow.compile()


graph = create_book_agent_graph()

result = graph.invoke(
    {
        "messages": [HumanMessage(content="есть ли книга в бд 'Harry Potter and the Prisoner of Azkaban'?")],
    }
)
print(result["messages"][-1].content)
