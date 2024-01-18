from pydantic import BaseModel, conint
from schemas.book import BookInfo
from schemas.library import LibraryResponse


class LibraryBookBase(BaseModel):
    library_id: int
    book_id: int
    available_count: int


class LibraryBookFilter(BaseModel):
    library_id: int | None = None
    book_id: int | None = None
    available_count: int | None = None


class LibraryBookUpdate(BaseModel):
    library_id: conint(ge=1) | None = None
    book_id: conint(ge=1) | None = None
    available_count: conint(ge=0) | None = None


class LibraryBookCreate(LibraryBookBase):
    pass


class LibraryBook(LibraryBookBase):
    id: int


class LibraryBookResponse(LibraryBookBase):
    id: int
    library: LibraryResponse
    book: BookInfo


class LibraryBookPaginationResponse(BaseModel):
  page: conint(ge=1)
  pageSize: conint(ge=1)
  totalElements: conint(ge=0)
  items: list[LibraryBookResponse]
