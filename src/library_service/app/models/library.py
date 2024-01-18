from uuid import uuid4
from sqlalchemy import UUID, Column, Integer, String

from utils.database import Base


class LibraryModel(Base):
  __tablename__ = "library"
  __table_args__ = {'extend_existing': True}
  
  id          = Column(Integer, primary_key=True, index=True)
  library_uid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
  name        = Column(String(80), unique=True, nullable=False)
  city        = Column(String(255), nullable=False)
  address     = Column(String(255), nullable=False)
