from uuid import UUID
from sqlalchemy.orm import Session

from cruds.library import LibraryCRUD
from schemas.library import LibraryFilter, LibraryUpdate, LibraryCreate, LibraryResponse, LibraryPaginationResponse
from exceptions.http import NotFoundException, ConflictException
from models.library import LibraryModel


class LibraryService():
  def __init__(self, libraryCRUD: LibraryCRUD, db: Session):
    self._libraryCRUD: LibraryCRUD = libraryCRUD(db)

  async def get_all(
      self,
      filter: LibraryFilter,
      page: int = 1,
      size: int = 100,
  ) -> LibraryPaginationResponse:
    libs: list[LibraryModel]
    totalItems: int
    libs, totalItems = await self._libraryCRUD.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )

    libItems: list[LibraryResponse] = []
    for lib in libs:
      libItems.append(
        LibraryResponse(
          name=lib.name,
          city=lib.city,
          address=lib.address,
          library_uid=lib.library_uid,
        )
      )

    return LibraryPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=totalItems,
      items=libItems,
    )
  
  async def get_by_uid(
      self, 
      uid: UUID,
  ):
    library = await self._libraryCRUD.get_by_uid(uid)
    if library is None:
      raise NotFoundException(prefix="get library")
    
    return library

  async def create(
      self,
      library_create: LibraryCreate,
  ):
    library = LibraryModel(**library_create.model_dump())
    library = await self._libraryCRUD.create(library)
    if library is None:
      raise ConflictException(prefix="create library")
    
    return library
  
  async def patch(
      self,
      uid: UUID,
      library_patch: LibraryUpdate,
  ):
    library = await self._libraryCRUD.get_by_uid(uid)
    if library is None:
      raise NotFoundException(prefix="patch library")
    
    library = await self._libraryCRUD.update(library, library_patch)
    if library is None:
      raise ConflictException(prefix="patch library")
    
    return library
  
  async def delete(
      self,
      uid: UUID,
  ):
    library = await self._libraryCRUD.get_by_uid(uid)
    if library is None:
      raise NotFoundException(prefix="delete library")
    
    return await self._libraryCRUD.delete(library)
