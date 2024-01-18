from enum import Enum

from schemas.response import ErrorResponse, ValidationErrorResponse


class RespLibraryEnum(Enum):
  GetAll = {
    "description": "All Library",
  }
  GetByUID = {
    "description": "Library by uid",
  }
  Created = {
    "description": "Created new Library",
    "headers": {
      "Location": {
        "description": "Path to new Library",
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
    "description": "Library by uid was removed",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
  Patch = {
    "description": "Library by uid was updated",
  }


  InvalidData = {
    "model": ValidationErrorResponse,
    "description": "Invalid data",
  }
  NotFound = {
    "model": ErrorResponse,
    "description": "Not found Library by uid",
  }
  Conflict = {
    "model": ErrorResponse,
    "description": "Conflict",
  }


class RespBookEnum(Enum):
  GetAll = {
    "description": "All Book",
  }
  GetByUID = {
    "description": "Book by uid",
  }
  Created = {
    "description": "Created new Book",
    "headers": {
      "Location": {
        "description": "Path to new Book",
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
    "description": "Book by uid was removed",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
  Patch = {
    "description": "Book by uid was updated",
  }


  InvalidData = {
    "model": ValidationErrorResponse,
    "description": "Invalid data",
  }
  NotFound = {
    "model": ErrorResponse,
    "description": "Not found Book by uid",
  }
  Conflict = {
    "model": ErrorResponse,
    "description": "Conflict",
  }


class RespLibraryBookEnum(Enum):
  GetAll = {
    "description": "All LibraryBook",
  }
  GetByID = {
    "description": "LibraryBook by id",
  }
  Created = {
    "description": "Created new LibraryBook",
    "headers": {
      "Location": {
        "description": "Path to new LibraryBook",
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
    "description": "LibraryBook by id was removed",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
  Patch = {
    "description": "LibraryBook by id was updated",
  }


  InvalidData = {
    "model": ValidationErrorResponse,
    "description": "Invalid data",
  }
  NotFound = {
    "model": ErrorResponse,
    "description": "Not found LibraryBook by id",
  }
  Conflict = {
    "model": ErrorResponse,
    "description": "Conflict",
  }


class RespManageEnum(Enum):
  Health = {
    "description": "Library server is ready to work",
    "content": {
      "application/octet-stream": {
        "example": ""
      }
    },
  }
