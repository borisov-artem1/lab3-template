from uuid import UUID
from sqlalchemy.orm import Session, Query

from schemas.book import BookFilter, BookUpdate
from models.book import BookModel


class BookCRUD():
  def __init__(self, db: Session):
    self._db = db

  async def get_all(
      self,
      filter: BookFilter,
      offset: int = 0,
      limit: int = 100,
  ) -> list[BookModel]:
    books = self._db.query(BookModel)
    books = await self.__filter_books(books, filter)
    return books.offset(offset).limit(limit).all()
  
  async def get_by_uid(self, uid: UUID) -> BookModel | None:
    return self._db.query(BookModel).filter(BookModel.book_uid == uid).first()
  
  async def create(self, book: BookModel) -> BookModel | None:
    try:
      self._db.add(book)
      self._db.commit()
      self._db.refresh(book)
    except:
      return None
    
    return book
  
  async def update(self, book: BookModel, book_update: BookUpdate) -> BookModel | None:
    update_fields = book_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
      setattr(book, key, value)

    try:
      self._db.add(book)
      self._db.commit()
      self._db.refresh(book)
    except:
      return None
    
    return book
  
  async def delete(self, book: BookModel) -> BookModel:
    self._db.delete(book)
    self._db.commit()

    return book

  async def __filter_books(
      self,
      books: Query[BookModel],
      filter: BookFilter
    ) -> Query[BookModel]:
    if filter.author:
      books.filter(BookModel.author == filter.author)

    if filter.genre:
      books.filter(BookModel.genre == filter.genre)

    if filter.name:
      books.filter(BookModel.name == filter.name)
    
    if filter.condition:
      books.filter(BookModel.condition == filter.condition)

    return books
