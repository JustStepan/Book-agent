import json
from openai import OpenAI
from langchain_core.messages import AIMessage, ToolMessage

import tools
from utils import msg_convertor
from schema import BookAgentState
from settings import settings


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="dummy-key",
)


def llm_node(state: BookAgentState):
    messages = msg_convertor(state['messages'])
    full_messages = [
        {"role": "system", "content": settings.prompts['query']['system']},
    ] + messages

    response = client.chat.completions.create(
        model=settings.model,
        messages=full_messages,
        temperature=0.1,
        tools=tools.TOOLS_DESCRIPTION,
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

    if hasattr(tools, func_name):

        func = getattr(tools, func_name)
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
