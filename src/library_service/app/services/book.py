from uuid import UUID
from sqlalchemy.orm import Session

from cruds.book import BookCRUD
from schemas.book import BookFilter, BookUpdate, BookCreate
from exceptions.http import NotFoundException, ConflictException
from models.book import BookModel


class BookService():
  def __init__(self, bookCRUD: BookCRUD, db: Session):
    self._bookCRUD: BookCRUD = bookCRUD(db)

  async def get_all(
      self,
      filter: BookFilter,
      page: int = 1,
      size: int = 100,
  ):
    return await self._bookCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
  
  async def get_by_uid(
      self, 
      uid: UUID,
  ):
    book = await self._bookCRUD.get_by_uid(uid)
    if book is None:
      raise NotFoundException(prefix="get book")
    
    return book

  async def create(
      self,
      book_create: BookCreate,
  ):
    book = BookModel(**book_create.model_dump())
    book = await self._bookCRUD.create(book)
    if book is None:
      raise ConflictException(prefix="create book")
    
    return book
  
  async def patch(
      self,
      uid: UUID,
      book_patch: BookUpdate,
  ):
    book = await self._bookCRUD.get_by_uid(uid)
    if book is None:
      raise NotFoundException(prefix="patch book")
    
    book = await self._bookCRUD.update(book, book_patch)
    if book is None:
      raise ConflictException(prefix="patch book")
    
    return book
  
  async def delete(
      self,
      uid: UUID,
  ):
    book = await self._bookCRUD.get_by_uid(uid)
    if book is None:
      raise NotFoundException(prefix="delete book")
    
    return await self._bookCRUD.delete(book)
