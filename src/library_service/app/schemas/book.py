from pydantic import BaseModel, constr, conint
from uuid import UUID

from enums.status import ConditionStatus


class BookBase(BaseModel):
    name: constr(max_length=255)
    author: constr(max_length=255)
    genre: constr(max_length=255)
    condition: ConditionStatus


class BookFilter(BaseModel):
    name: constr(max_length=255) | None = None
    author: constr(max_length=255) | None = None
    genre: constr(max_length=255) | None = None
    condition: ConditionStatus | None = None
    

class BookUpdate(BaseModel):
    name: constr(max_length=255) | None = None
    author: constr(max_length=255) | None = None
    genre: constr(max_length=255) | None = None
    condition: ConditionStatus | None = None


class BookCreate(BookBase):
    condition: ConditionStatus = "EXCELLENT"


class Book(BookBase):
    id: int
    book_uid: UUID


class BookInfo(BookBase):
  book_uid: UUID


class BookPaginationResponse(BaseModel):
  page: conint(ge=1)
  pageSize: conint(ge=1)
  totalElements: conint(ge=0)
  items: list[BookInfo]
