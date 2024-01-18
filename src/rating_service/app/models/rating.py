from sqlalchemy import UUID, Column, Integer, String, CheckConstraint

from utils.database import Base


class RatingModel(Base):
  __tablename__ = "rating"
  __table_args__ = {'extend_existing': True}
  
  id        = Column(Integer, primary_key=True, index=True)
  username  = Column(String(80), nullable=False)
  stars     = Column(Integer, CheckConstraint("stars BETWEEN 0 AND 100"), default=0)
