from sqlalchemy.orm import Session, Query

from schemas.library_book import LibraryBookFilter, LibraryBookUpdate
from models.library_book import LibraryBookModel


class LibraryBookCRUD():
  def __init__(self, db: Session):
    self._db = db

  async def get_all(
      self,
      filter: LibraryBookFilter,
      offset: int = 0,
      limit: int = 100,
  ) -> list[LibraryBookModel]:
    library_books = self._db.query(LibraryBookModel).join(LibraryBookModel.book).join(LibraryBookModel.library)
    library_books = await self.__filter_library_books(library_books, filter)
    total = library_books.count()

    return library_books.offset(offset).limit(limit).all(), total
  
  async def get_by_id(self, id: int) -> LibraryBookModel | None:
    return self._db.query(LibraryBookModel).filter(LibraryBookModel.id == id).first()
  
  async def create(self, library_book: LibraryBookModel) -> LibraryBookModel | None:
    try:
      self._db.add(library_book)
      self._db.commit()
      self._db.refresh(library_book)
    except:
      return None
    
    return library_book
  
  async def update(self, library_book: LibraryBookModel, library_book_update: LibraryBookUpdate) -> LibraryBookModel | None:
    update_fields = library_book_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
      setattr(library_book, key, value)

    try:
      self._db.add(library_book)
      self._db.commit()
      self._db.refresh(library_book)
    except:
      return None
    
    return library_book
  
  async def delete(self, library_book: LibraryBookModel) -> LibraryBookModel:
    self._db.delete(library_book)
    self._db.commit()

    return library_book

  async def __filter_library_books(
      self,
      library_books: Query[LibraryBookModel],
      filter: LibraryBookFilter
    ) -> Query[LibraryBookModel]:
    if filter.book_id:
      library_books = library_books.filter(LibraryBookModel.book_id == filter.book_id)

    if filter.library_id:
      library_books = library_books.filter(LibraryBookModel.library_id == filter.library_id)

    if filter.available_count:
      library_books = library_books.filter(LibraryBookModel.available_count == filter.available_count)

    return library_books
