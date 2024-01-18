from uuid import uuid4
from sqlalchemy import UUID, Column, Integer, String, CheckConstraint

from utils.database import Base


class BookModel(Base):
  __tablename__ = "book"
  __table_args__ = {'extend_existing': True}
  
  id        = Column(Integer, primary_key=True, index=True)
  book_uid  = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
  name      = Column(String(255), nullable=False)
  author    = Column(String(255), nullable=False)
  genre     = Column(String(255), nullable=False)
  condition = Column(String(20), CheckConstraint("condition IN ('EXCELLENT', 'GOOD', 'BAD')"), default='EXCELLENT')
