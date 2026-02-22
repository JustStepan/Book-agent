from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from schema import SearchRequest
from graph import graph


app = FastAPI()


@app.get('/')
def health_check():
    return {'message': "Все OK, Бро!"}


@app.post('/search')
def get_user_request(request: SearchRequest):
    result = graph.invoke(
        {
            "messages": [HumanMessage(content=request.user_message)],
        }
    )
    return {'message': result["messages"][-1].content}