"""Здесь представлена и связь один ко многим автор/книги
и связь многие ко многим жанры/книги"""

from sqlalchemy import CheckConstraint, Column, Float, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

book_genre_association = Table(
    'book_genre', 
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.id'), primary_key=True)
)


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Связь "один ко многим": у одного автора много книг
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    year = Column(Integer, nullable=False)
    genres = relationship("Genre", secondary=book_genre_association,  back_populates="books")
    rating = Column(Float)
    description = Column(Text)

    author = relationship("Author", back_populates="books")

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 10', name='check_rating_range'),
    )

    def __repr__(self):
        return f"<Book(author='{self.author.name}', title='{self.title}', year={self.year})>"


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    books = relationship("Book", secondary=book_genre_association,  back_populates="genres")
