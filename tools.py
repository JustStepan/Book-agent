from typing import List, Union
from ChromaDB import search_books_by_meaning
from db_execute import get_all_books, get_books_by_author, get_book_by_title, get_min_description, del_one_book
from fake_db import fill_db
from schema import Book


def search_by_meaning(query: str, n_books: int = 3) -> List[dict[str, Union[int, float, str]]]:
    return search_books_by_meaning(query, n_books)

def del_book(book_id: int)-> dict:
    return del_one_book(book_id)

def find_smallest_description() -> int:
    return get_min_description()


def books_by_author(author: str) -> dict:
    return get_books_by_author(author)


def book_by_title(q_title: str) -> dict:
    return get_book_by_title(q_title)


def get_amount_books() -> int:
    return len(get_all_books())


def new_books_db(amount: int) -> List[Book]:
    return fill_db(amount)


TOOLS_DESCRIPTION = [
    {
        "type": "function",
        "function": {
            "name": "search_by_meaning",
            "description": """Семантический поиск книг по смыслу, теме или настроению.
Используй когда пользователь описывает что хочет почитать, а не называет
конкретную книгу. Перед передачей в query — расширь запрос пользователя:
добавь синонимы, тематику, жанр, настроение.
Например: 'про войну' → 'военный роман, сражения, героизм, исторический конфликт'""",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Улучшенный запрос пользователя на поиск книг по смыслу. Можно расширить для лучшего поиска."
                    },
                    "n_books": {
                        "type": "integer",
                        "description": "количество ворзвращаемых книг (Опционально, только если пользователь просит)"
                    },
                },
                "required": ["query"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_smallest_description",
            "description": "Функция возвращает словарь с id и description книги с наименьшим описанием в БД",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_by_title",
            "description": "Функция возвращает параметры книги по ее названию",
            "parameters": {
                "type": "object",
                "properties": {
                    "q_title": {
                        "type": "string",
                        "description": "Название книги на русском или английским языках (зависит от того как было приведено в запросе)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_amount_books",
            "description": "Возвращает общее количество книг, содержащихся в базе данных. Вызывается без аргументов.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "books_by_author",
            "description": "Функция возвращает книги автора",
            "parameters": {
                "type": "object",
                "properties": {
                    "author": {
                        "type": "string",
                        "description": "Имя автора книги в формате Имя Фамилия (например Л. Толстой) на английском или русском языках (зависит от того как было приведено в запросе)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "new_books_db",
            "description": "Функция генерирует заданное количество книг. Возвращает список pydantic объектов этой книги(книг).",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "Количество книг, которе пользователь попросил сгенерировать"
                    }
                },
                "required": ["amount"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "del_book",
            "description": "Удаляет книгу по ее id из базы данных",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "номер книги (id) в базе данных"
                    }
                },
                "required": ["book_id"]
            }
        }
    },
]