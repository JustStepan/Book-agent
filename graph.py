from schema import BookAgentState
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END
import json
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fake_db import fill_db
import tools as tl
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
from prompts import PROMPTS
from schema import Book, SearchResult, SearchRequest


app = FastAPI(title='Book-agent')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="dummy-key",
)

user_message = 'Сколько книг в БД?'


@app.post("/search2", response_model=SearchResult)
def llm_node(state: BookAgentState) -> dict:
    messages = state["messages"]
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": PROMPTS['query']['system']},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        tools=tl.TOOLS_DESCRIPTION,  # type: ignore[arg-type]
        tool_choice="auto",
    )

    if not response.choices[0].message.tool_calls:
        return SearchResult(type="text", data=response.choices[0].message.content)

    tool_call: ChatCompletionMessageToolCall = response.choices[0].message.tool_calls[0]  # type: ignore[assignment]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    if not hasattr(tl, function_name):
        return SearchResult(type="error", data=f"Function {function_name} not found")

    func = getattr(tl, function_name)
    result = func(**arguments)
    print(result)

    if isinstance(result, list):
        books = [
            Book(
                author_name=book.author.name,
                book_title=book.title,
                year=book.year,
                genre_names=[g.title for g in book.genres],
                rating=book.rating,
                description=book.description,
            )
            for book in result
        ]
        return SearchResult(type="books", data=books)

    if isinstance(result, int):
        return SearchResult(type="count", data=result)

    return SearchResult(type="text", data=result)


@app.post("/generate", response_model=List[Book])
def generate_books(amount: int) -> List[Book]:
    return fill_db(amount)
