import json
from typing import Any, List
from openai import OpenAI
from db_execute import get_all_books, add_complete_book
from schema import Book
from settings import settings


def generate_books() -> dict[str, Any]:
    books = get_all_books()
    messages = [
        {"role": "system", "content": settings.prompts["fake"]["system"]},
        {
            "role": "user",
            "content": settings.prompts["fake"]["user"]
            + f"\nСписок книг которые генерировать не нужно здесь: {books}.",
        },
    ]

    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="dummy-key",
    )

    response = client.chat.completions.create(
        model=settings.model,
        messages=messages,
        temperature=0.6,
    )

    message = response.choices[0].message
    content = message.content or "" # Это нужно позже оформить в красивую функцию.
    if content := message.content:
        if "</think>" in content:
            content = content.split("</think>")[-1].strip()
        if "<|begin_of_box|>" in content:
            content = content.split("<|begin_of_box|>")[-1].strip()
        if "<|message|>" in content:
            content = content.split("<|message|>")[-1].strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON")
        return {}

    return {
        "author_name": data.get("author", "Без автора"),
        "book_title": data.get("title", "Без имени"),
        "year": data.get("year", "Без даты"),
        "genre_names": data.get("genres", "Без даты"),
        "rating": data.get("rating", "Без даты"),
        "description": data.get("description", "Без даты"),
    }


def fill_db(it) -> List[Book]:
    book_list = []
    for _ in range(it):
        data = generate_books()
        add_complete_book(**data)
        book_list.append(Book(**data))
    return book_list


if __name__ == "__main__":
    fill_db(1)
