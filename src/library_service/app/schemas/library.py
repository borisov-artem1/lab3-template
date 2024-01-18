from typing import List
from pydantic import BaseModel, conint, constr
from uuid import UUID


class LibraryBase(BaseModel):
    name: constr(max_length=80)
    city: constr(max_length=255)
    address: constr(max_length=255)


class LibraryFilter(BaseModel):
    name: constr(max_length=80) | None = None
    city: constr(max_length=255) | None = None
    address: constr(max_length=255) | None = None
    

class LibraryUpdate(BaseModel):
    name: constr(max_length=80) | None = None
    city: constr(max_length=255) | None = None
    address: constr(max_length=255) | None = None


class LibraryCreate(LibraryBase):
    name: constr(max_length=80) | None = None
    city: constr(max_length=255) | None = None
    address: constr(max_length=255) | None = None


class Library(LibraryBase):
    id: int
    library_uid: UUID


class LibraryResponse(LibraryBase):
  library_uid: UUID


class LibraryPaginationResponse(BaseModel):
  page: conint(ge=1)
  pageSize: conint(ge=1)
  totalElements: conint(ge=0)
  items: list[LibraryResponse]
