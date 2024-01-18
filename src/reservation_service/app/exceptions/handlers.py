from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse


async def http_exception_handler(
    request: Request,
    exception: HTTPException,
):
  return JSONResponse(
    status_code=exception.status_code,
    content={
      "message": exception.detail,
    }
  )


async def request_validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
  errors = jsonable_encoder(exception.errors())
  errors_detail = []

  for err in errors:
    details = {}
    details["type"] = err["type"]
    details["msg"] = err["msg"]
    details["loc"] = " -> ".join(map(str, err["loc"]))

    errors_detail.append(details)

  return JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content={
      "message": "Invalid request",
      "errors": errors_detail,
    }
  )