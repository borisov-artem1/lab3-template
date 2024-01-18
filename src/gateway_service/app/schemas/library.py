from pydantic import BaseModel, conint, constr
from uuid import UUID

from enums.status import ConditionStatus


# ======= Library =======
class LibraryBase(BaseModel):
  name: constr(max_length=80) | None
  city: constr(max_length=255) | None
  address: constr(max_length=255) | None


class LibraryFilter(BaseModel):
  name: constr(max_length=80) | None = None
  city: constr(max_length=255) | None = None
  address: constr(max_length=255) | None = None


class Library(LibraryBase):
  id: int
  library_uid: UUID


class LibraryResponse(LibraryBase):
  libraryUid: UUID | None


class LibraryPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: list[LibraryResponse]


# ======= Book =======
class BookBase(BaseModel):
  name: constr(max_length=255) | None
  author: constr(max_length=255) | None
  genre: constr(max_length=255) | None
  condition: ConditionStatus | None


class BookUpdate(BaseModel):
  name: constr(max_length=255) | None = None
  author: constr(max_length=255) | None = None
  genre: constr(max_length=255) | None = None
  condition: ConditionStatus | None = None


class Book(BookBase):
  id: int
  bookUid: UUID


class BookInfo(BookBase):
  bookUid: UUID | None


class BookPaginationResponse(BaseModel):
  page: conint(ge=1)
  pageSize: conint(ge=1)
  totalElements: conint(ge=0)
  items: list[BookInfo]


# ===== LibraryBookEntity =====
class LibraryBookEntityBase(BaseModel):
  libraryId: int
  bookId: int
  availableCount: int


class LibraryBookUpdate(BaseModel):
  library_id: conint(ge=1) | None = None
  book_id: conint(ge=1) | None = None
  available_count: conint(ge=0) | None = None


class LibraryBookEntity(LibraryBookEntityBase):
    id: int


class LibraryBookEntityResponse(LibraryBookEntityBase):
  id: int
  library: LibraryResponse
  book: BookInfo



# ===== LibraryBook =====
class LibraryBookResponse(BookBase):
  bookUid: UUID
  availableCount: int


class LibraryBookPaginationResponse(BaseModel):
  page: int
  pageSize: int
  totalElements: int
  items: list[LibraryBookResponse]
