from fastapi import HTTPException, status


class NotFoundException(HTTPException):
  def __init__(
    self,
    prefix: str,
    headers: dict[str, str] | None = None,
  ) -> None:
    super().__init__(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"{prefix}: объекта с таким id не существует",
      headers=headers,
    )

class ConflictException(HTTPException):
  def __init__(
      self,
    prefix: str,
    headers: dict[str, str] | None = None,
  ) -> None:
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"{prefix}: объект с таким(и) атрибутом(ами) уже существует",
      headers=headers,
    )
