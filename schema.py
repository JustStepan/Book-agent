from typing import Any, List, TypedDict, Annotated
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


class BookAgentState(TypedDict):
    messages: Annotated[list, add_messages]


class LLMBookCreate(BaseModel):

    author: str = Field(..., min_length=5, max_length=30, description='Автор книги в формате Имя Фамилия, например: Л. Толстой')
    title: str = Field(..., min_length=3, max_length=100, description='Наименование книги')
    year: int = Field(..., max_length=4, description='Год написания произведения')
    genres: List[str] = Field(..., max_length=10, description='Жанры книги, например: ["Фантастика", "Роман", "Эпопея", "Научное"]')
    rating: float = Field(..., gt=0, lt=10.0, description='Рейтинг книги в float формате. Значения варьюруются от 0 до 10. Например: 6.7.')
    description: str = Field(..., max_length=1000, description='Обширное произведение произведения: его сильные и слабые стороны, кому подойдет, для кого написано.')


class Book(BaseModel):
    author_name: str
    book_title: str
    year: int
    genre_names: List[str]
    rating: float
    description: str

class SearchResult(BaseModel):
    type: str  # "books" | "count" | "text" | "error"
    data: Any


class SearchRequest(BaseModel):
    user_message: str = Field(..., min_length=1, description="Поисковый запрос пользователя")