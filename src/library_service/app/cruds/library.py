from uuid import UUID
from sqlalchemy.orm import Session, Query

from schemas.library import LibraryFilter, LibraryUpdate
from models.library import LibraryModel


class LibraryCRUD():
  def __init__(self, db: Session):
    self._db = db

  async def get_all(
      self,
      filter: LibraryFilter,
      offset: int = 0,
      limit: int = 100,
  ) -> [list[LibraryModel], int]:
    libs = self._db.query(LibraryModel)
    libs = await self.__filter_libraries(libs, filter)
    total = libs.count()

    return libs.offset(offset).limit(limit).all(), total
  
  async def get_by_uid(self, uid: UUID) -> LibraryModel | None:
    return self._db.query(LibraryModel).filter(LibraryModel.library_uid == uid).first()
  
  async def create(self, library: LibraryModel) -> LibraryModel | None:
    try:
      self._db.add(library)
      self._db.commit()
      self._db.refresh(library)
    except:
      return None
    
    return library
  
  async def update(self, library: LibraryModel, library_update: LibraryUpdate) -> LibraryModel | None:
    update_fields = library_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
      setattr(library, key, value)

    try:
      self._db.add(library)
      self._db.commit()
      self._db.refresh(library)
    except:
      return None
    
    return library
  
  async def delete(self, library: LibraryModel) -> LibraryModel:
    self._db.delete(library)
    self._db.commit()

    return library

  async def __filter_libraries(
      self,
      libraries: Query[LibraryModel],
      filter: LibraryFilter
    ) -> Query[LibraryModel]:
    if filter.address:
      libraries = libraries.filter(LibraryModel.address == filter.address)

    if filter.city:
      libraries = libraries.filter(LibraryModel.city == filter.city)

    if filter.name:
      libraries = libraries.filter(LibraryModel.name == filter.name)

    return libraries
