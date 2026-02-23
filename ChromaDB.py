import pprint

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


def search_books_by_meaning(query: str, n_results: int) -> list:
    query = query.lower().strip()
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    ids_list = results['ids'][0]
    docs_list = results['documents'][0]
    dists_list = results['distances'][0]
    metas_list = results['metadatas'][0]

    final_results = []

    for i in range(len(ids_list)):
        final_results.append({
            "rank": i + 1,  # Место в выборке (начинаем с 1)
            "score": dists_list[i],  # Расстояние (косинусное)
            "db_id": ids_list[i],
            "documents": docs_list[i],
            "metadatas": metas_list[i],
            "description": f"{i + 1} место в выборке с результатом косинусного совпадения: {dists_list[i]}"
        })

    return final_results


pprint.pprint(search_books_by_meaning('кот мурзилка в башне', 5))
