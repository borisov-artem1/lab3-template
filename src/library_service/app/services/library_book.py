from sqlalchemy.orm import Session

from cruds.library_book import LibraryBookCRUD
from schemas.library_book import LibraryBookFilter, LibraryBookUpdate, LibraryBookCreate, LibraryBookPaginationResponse, LibraryBookResponse
from schemas.library import LibraryResponse
from schemas.book import BookInfo

from exceptions.http import NotFoundException, ConflictException
from models.library_book import LibraryBookModel
from models.library import LibraryModel
from models.book import BookModel


class LibraryBookService():
  def __init__(self, library_bookCRUD: LibraryBookCRUD, db: Session):
    self._library_bookCRUD: LibraryBookCRUD = library_bookCRUD(db)

  async def get_all(
      self,
      filter: LibraryBookFilter,
      page: int = 1,
      size: int = 100,
  ) -> LibraryBookPaginationResponse:
    
    library_books: list[LibraryBookModel]
    total_elements: int
    library_books, total_elements = await self._library_bookCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
    library_book_items: list[LibraryBookResponse] = []
    for library_book in library_books:
      library_model: LibraryModel = library_book.library
      book_model: BookModel = library_book.book

      library: LibraryResponse = LibraryResponse(
        name=library_model.name,
        city=library_model.city,
        address=library_model.address,
        library_uid=library_model.library_uid
      )

      book: BookInfo = BookInfo(
        name=book_model.name,
        author=book_model.author,
        genre=book_model.genre,
        condition=book_model.condition,
        book_uid=book_model.book_uid,
      )

      library_book_items.append(
        LibraryBookResponse(
          library_id=library_book.library_id,
          book_id=library_book.book_id,
          available_count=library_book.available_count,
          id=library_book.id,
          library=library,
          book=book,
        )
      )

    return LibraryBookPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=total_elements,
      items=library_book_items,
    )
  
  async def get_by_id(
      self, 
      id: int,
  ):
    library_book = await self._library_bookCRUD.get_by_id(id)
    if library_book is None:
      raise NotFoundException(prefix="get library_book")
    
    return library_book

  async def create(
      self,
      library_book_create: LibraryBookCreate,
  ):
    library_book = LibraryBookModel(**library_book_create.model_dump())
    library_book = await self._library_bookCRUD.create(library_book)
    if library_book is None:
      raise ConflictException(prefix="create library_book")
    
    return library_book
  
  async def patch(
      self,
      id: int,
      library_book_patch: LibraryBookUpdate,
  ):
    library_book = await self._library_bookCRUD.get_by_id(id)
    if library_book is None:
      raise NotFoundException(prefix="patch library_book")
    
    library_book = await self._library_bookCRUD.update(library_book, library_book_patch)
    if library_book is None:
      raise ConflictException(prefix="patch library_book")
    
    return library_book
  
  async def delete(
      self,
      id: int,
  ):
    library_book = await self._library_bookCRUD.get_by_id(id)
    if library_book is None:
      raise NotFoundException(prefix="delete library_book")
    
    return await self._library_bookCRUD.delete(library_book)
