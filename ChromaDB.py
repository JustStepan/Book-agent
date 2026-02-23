import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# 1. Создаём клиент (persistent — сохраняется на диск)
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Embedding функция — ChromaDB вызывает её автоматически
embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)


def get_collection():
    return client.get_or_create_collection(
        name="books",
        embedding_function=embedding_fn
    )


def search_books_by_meaning(query: str, n_results: int = 3) -> list:
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
    # return {
    #     "documents": results["documents"],
    #     "metadatas": results["metadatas"],
    #     "distances": results["distances"],
    # }

print(search_books_by_meaning('воспоминание', 5))