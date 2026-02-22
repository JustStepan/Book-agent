from typing import List
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, joinedload
from models import Author, Book, Genre
from pathlib import Path

BASE_DIR = Path(__file__).parent
engine = create_engine(f"sqlite:///{BASE_DIR}/local_db.sqlite")
Session = sessionmaker(bind=engine)


def del_one_book(id: int) -> dict:
    with Session() as session:
        try:
            book = session.execute(
                select(Book).filter_by(id=id)
            ).scalar_one_or_none()

            if not book:
                return {'result': 'Ошибка', 'message': 'Книга не найдена'}

            session.delete(book)
            session.commit()
            return {'result': f'Книга с id={id} успешно удалена'}

        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при удалении книги с id {id}: {e}")
            return {'result': 'Ошибка', 'message': str(e)}


def get_min_description():
    with Session() as session:
        stmt = select(Book.id, Book.description, Book.title)
        
        # .mappings() говорит SQLAlchemy вернуть результаты как словари
        # result будет списком вида: [{'id': 1, 'description': '...'}, {'id': 2, 'description': '...'}]
        result = session.execute(stmt).mappings().all()
        min_description_len = sorted(result, key=lambda x: len(x['description']))[0]
        print(min_description_len)
        return min_description_len



def get_all_books():
    with Session() as session:
        query = select(Book).options(
            joinedload(Book.author), joinedload(Book.genres)
        )
        result = session.execute(query)
        books = (
            result.scalars().unique().all()
        )
    return books


def add_complete_book(
    author_name: str,
    book_title: str,
    year: int,
    genre_names: List[str],
    rating: float,
    description: str,
):
    """Наполняем БД данными в стиле SQLAlchemy 2.0"""

    # Используем SessionLocal или sessionmaker, созданный ранее
    with Session() as session:
        try:
            # 1. Работаем с АВТОРОМ (Style 2.0: select)
            author = session.execute(
                select(Author).filter_by(name=author_name)
            ).scalar_one_or_none()

            if not author:
                author = Author(name=author_name)
                session.add(author)

            # 2. Работаем с ЖАНРАМИ (Many-to-Many)
            genres_list = []
            for g_name in genre_names:
                genre = session.execute(
                    select(Genre).filter_by(title=g_name)
                ).scalar_one_or_none()

                if not genre:
                    genre = Genre(title=g_name)
                    session.add(genre)
                genres_list.append(genre)

            # 3. Создаем КНИГУ
            new_book = Book(
                title=book_title,
                year=year,
                rating=rating,
                description=description,
                author=author,
                genres=genres_list,
            )

            session.add(new_book)

            # 4. Фиксируем транзакцию
            session.commit()
            print(f"✅ Успешно: '{book_title}' (Автор: {author.name})")
            return new_book

        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при добавлении: {e}")


def get_books_by_author(author_name: str) -> list[Book]:
    with Session() as session:
        # 1. Используем join, чтобы фильтровать по имени в связанной таблице
        query = (
            select(Book)
            .join(Book.author)
            .options(joinedload(Book.author), joinedload(Book.genres))
            .where(
                Author.name == author_name
            )  # Фильтруем по колонке класса Author
        )

        result = session.execute(query)

        # 2. scalars().unique().all() — стандарт для связей Many-to-Many
        books = result.scalars().unique().all()

    return books


def get_book_by_title(q_title: str) -> list[Book]:
    with Session() as session:
        query = (
            select(Book)
            .options(joinedload(Book.author), joinedload(Book.genres))
            .where(Book.title == q_title)
        )

        result = session.execute(query)

        # 2. scalars().unique().all() — стандарт для связей Many-to-Many
        books = result.scalars().unique().all()

    return books

