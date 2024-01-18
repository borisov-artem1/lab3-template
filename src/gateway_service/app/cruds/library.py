import json
from uuid import UUID
import requests
from requests import Response

from cruds.base import BaseCRUD
from utils.settings import get_settings
from schemas.library import (
  LibraryResponse,
  BookInfo,
  LibraryBookEntityResponse,
  LibraryPaginationResponse,
  LibraryBookUpdate,
  BookUpdate,
)


class LibraryCRUD(BaseCRUD):
  def __init__(self):
    settings = get_settings()
    library_host = settings["services"]["gateway"]["library_host"]
    library_port = settings["services"]["library"]["port"]

    self.http_path = f'http://{library_host}:{library_port}/api/v1/'

  async def get_all_libraries(
      self,
      page: int = 1,
      size: int = 100,
      city: str | None = None,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}library/?page={page}&size={size}'\
        f'{f"&city={city}" if city else ""}'
    )
    self._check_status_code(response.status_code)
    
    libraries_json = response.json()
    libraries = libraries_json["items"]

    library_items: list[LibraryResponse] = []
    for library in libraries:
      library_items.append(
        LibraryResponse(
          libraryUid=library["library_uid"],
          name=library["name"],
          address=library["address"],
          city=library["city"],
        )
      )

    return LibraryPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=libraries_json["totalElements"],
      items=library_items,
    )
  

  async def get_all_library_books(
      self,
      page: int = 1,
      size: int = 100,
  ) -> list[LibraryBookEntityResponse]:
    response: Response = requests.get(
      url=f'{self.http_path}library_book/?page={page}&size={size}'
    )
    self._check_status_code(response.status_code)

    library_books_json = response.json()
    library_books = library_books_json["items"]

    library_book_items: list[LibraryBookEntityResponse] = []
    for library_book in library_books:
      library_book_items.append(
        LibraryBookEntityResponse(
          id=library_book["id"],
          libraryId=library_book["library_id"],
          bookId=library_book["book_id"],
          availableCount=library_book["available_count"],
          library=LibraryResponse(
            libraryUid=library_book["library"]["library_uid"],
            name=library_book["library"]["name"],
            address=library_book["library"]["address"],
            city=library_book["library"]["city"],
          ),
          book=BookInfo(
            bookUid=library_book["book"]["book_uid"],
            name=library_book["book"]["name"],
            author=library_book["book"]["author"],
            genre=library_book["book"]["genre"],
            condition=library_book["book"]["condition"],
          )
        )
      )

    return library_book_items
  

  async def get_library_by_uid(
      self,
      uid: UUID,
  ) -> LibraryResponse:
    response: Response = requests.get(
      url=f'{self.http_path}library/{uid}',
    )
    self._check_status_code(response.status_code)

    library_json = response.json()

    return LibraryResponse(
      libraryUid=library_json["library_uid"],
      name=library_json["name"],
      city=library_json["city"],
      address=library_json["address"],
    )
  

  async def get_book_by_uid(
      self,
      uid: UUID,
  ) -> BookInfo:
    response: Response = requests.get(
      url=f'{self.http_path}book/{uid}',
    )
    self._check_status_code(response.status_code)

    book_json = response.json()

    return BookInfo(
      bookUid=book_json["book_uid"],
      name=book_json["name"],
      author=book_json["author"],
      genre=book_json["genre"],
      condition=book_json["condition"],
    )
  

  async def patch_library_book(
      self,
      id: int,
      update: LibraryBookUpdate,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}library_book/{id}',
      data=json.dumps(update.model_dump(exclude_unset=True))
    )
    self._check_status_code(response.status_code)

    library_book = response.json()
    return library_book["id"]
  

  async def patch_book(
      self,
      uid: UUID,
      update: BookUpdate,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}book/{uid}',
      data=json.dumps(update.model_dump(exclude_unset=True))
    )
    self._check_status_code(response.status_code)

    book = response.json()
    return book["book_uid"]
  
