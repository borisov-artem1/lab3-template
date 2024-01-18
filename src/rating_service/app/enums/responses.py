from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class RespRatingEnum(Enum):
  GetAll = {
    "description": "All Rating",
  }
  GetByUID = {
    "description": "Rating by id",
  }
  Created = {
    "description": "Created new Rating",
    "headers": {
      "Location": {
        "description": "Path to new Rating",
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
    "description": "Rating by id was removed",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
  Patch = {
    "description": "Rating by id was updated",
  }


  InvalidData = {
    "model": ValidationErrorResponse,
    "description": "Invalid data",
  }
  NotFound = {
    "model": ErrorResponse,
    "description": "Not found Rating by id",
  }
  Conflict = {
    "model": ErrorResponse,
    "description": "Conflict",
  }


class RespManageEnum(Enum):
  Health = {
    "description": "Rating server is ready to work",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
