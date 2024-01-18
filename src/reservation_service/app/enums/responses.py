from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class RespReservationEnum(Enum):
  GetAll = {
    "description": "All Reservation",
  }
  GetByUID = {
    "description": "Reservation by uid",
  }
  Created = {
    "description": "Created new Reservation",
    "headers": {
      "Location": {
        "description": "Path to new Reservation",
        "style": "simple",
        "schema": {
          "type": "string"
        }
      }
    },
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
  Delete = {
    "description": "Reservation by uid was removed",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
  Patch = {
    "description": "Reservation by uid was updated",
  }


  InvaluidData = {
    "model": ValidationErrorResponse,
    "description": "Invaluid data",
  }
  NotFound = {
    "model": ErrorResponse,
    "description": "Not found Reservation by uid",
  }
  Conflict = {
    "model": ErrorResponse,
    "description": "Conflict",
  }


class RespManageEnum(Enum):
  Health = {
    "description": "Reservation server is ready to work",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
