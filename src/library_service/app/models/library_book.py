from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.book import BookModel
from models.library import LibraryModel
from utils.database import Base


class LibraryBookModel(Base):
  __tablename__ = "library_book"
  __table_args__ = {'extend_existing': True}
  
  id              = Column(Integer, primary_key=True, index=True)
  book_id         = Column(Integer, ForeignKey(BookModel.id))
  library_id      = Column(Integer, ForeignKey(LibraryModel.id))
  available_count = Column(Integer, nullable=False)
  
  book            = relationship(BookModel, foreign_keys=[book_id])
  library         = relationship(LibraryModel, foreign_keys=[library_id])
