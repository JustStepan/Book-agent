from ChromaDB import get_collection
from db_execute import get_all_books


def embed_all_books():
    books = get_all_books()
    collection = get_collection()
    
    # Form lists of data
    ids = [str(book.id) for book in books]
    documents = [book.description for book in books]
    metadatas = [
        {
            "title": book.title,
            "author": book.author.name,
            "book_id": book.id
        }
        for book in books
    ]

    # add data to chroma
    collection.upsert(
        ids=ids,              # уникальный ID — строка, обязательно
        documents=documents,  # что эмбеддится
        metadatas=metadatas
    )


embed_all_books()