# 📚 Book Agent

AI-агент для работы с базой книг. Принимает запросы на естественном языке, самостоятельно выбирает нужный инструмент и возвращает результат.

## Что умеет

- Генерировать новые записи книг через LLM (используется SO)
- Искать книги по автору и названию
- Считать количество книг в базе
- Находить книги по смыслу запроса (семантический поиск)
- Удалять книги по ID

## Стек

**Backend:** Python, FastAPI, LangGraph, SQLAlchemy, ChromaDB  
**LLM:** OpenAI-совместимый API (LM Studio / Ollama)  
**Embeddings:** sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)  
**Frontend:** React, TypeScript, TailwindCSS  
**DB:** SQLite + ChromaDB (векторный поиск)

## Архитектура агента

```
User Request
     │
     ▼
 FastAPI /search
     │
     ▼
 LangGraph Graph
     │
     ├── llm_node     — LLM решает какой инструмент вызвать
     ├── tool_node    — выполняет инструмент
     └── should_continue — возвращаться к LLM или завершить
```

Граф работает в цикле: `llm → tool → llm → END`. LLM получает результат инструмента и формирует финальный ответ.

## Структура проекта

```
├── main.py          # FastAPI приложение
├── graph.py         # Сборка LangGraph графа
├── nodes.py         # Ноды: llm_node, tool_node, should_continue
├── tools.py         # Инструменты агента + их описание для LLM
├── utils.py         # Конвертер LangChain → OpenAI messages
├── ChromaDB.py      # Клиент ChromaDB, функция семантического поиска
├── emdeb_books.py   # Скрипт наполнения векторной БД
├── db_execute.py    # SQL запросы (SQLAlchemy)
├── fake_db.py       # Генерация книг через LLM
├── models.py        # SQLAlchemy модели (Author, Book, Genre)
├── schema.py        # Pydantic схемы + BookAgentState
├── settings.py      # Конфигурация (pydantic-settings)
├── prompts.py       # Системные промпты
├── migrations/      # Alembic миграции
└── frontend/        # React приложение
```

## Запуск

**Требования:** Python 3.12+, Node.js, LM Studio или Ollama

```bash
# 1. Установить зависимости
uv sync

# 2. Применить миграции
uv run alembic upgrade head

# 3. Наполнить базу книг. fill_db(1) - аргумент - количество книг
uv run python fake_db.py

# 4. Создать векторные эмбеддинги из описания книг
uv run python emdeb_books.py

# 5. Запустить сервер
uv run uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Модели БД

```
Author ──< Book >── Genre
           (M2M через book_genre)
```

`Author` → `Book` — один ко многим  
`Book` ↔ `Genre` — многие ко многим

## Семантический поиск

Описания книг эмбеддируются моделью `paraphrase-multilingual-MiniLM-L12-v2` и хранятся в ChromaDB. При запросе типа "хочу про приключения и месть" агент вызывает инструмент `search_by_meaning` — он находит книги с похожим смыслом без точного совпадения слов.

## Настройка

В `settings.py` выбери модель(предварительно скачав в ollama или LM Studio):

```python
MODELS = {
    'Q': 'qwen/qwen3-8b',       # рекомендуется
    'M': 'mistralai/devstral-small-2-2512',
    'DS': 'deepseek/deepseek-r1-0528-qwen3-8b',
}
```
Измени в pydantic класе, имя модели --> model: str = MODELS['Q']

LM Studio должен быть запущен на `http://localhost:1234`.

## API

```
GET  /          — healthcheck
POST /search    — запрос к агенту {"user_message": "..."}
```