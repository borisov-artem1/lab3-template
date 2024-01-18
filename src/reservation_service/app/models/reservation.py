from sqlalchemy import UUID, Column, Integer, String, CheckConstraint, DateTime
from uuid import uuid4
from datetime import datetime as dt

from utils.database import Base


class ReservationModel(Base):
  __tablename__ = "reservation"
  __table_args__ = {'extend_existing': True}
  
  id              = Column(Integer, primary_key=True, index=True)
  reservation_uid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
  username        = Column(String(80), nullable=False)
  book_uid        = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
  library_uid     = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
  status          = Column(String(20), CheckConstraint("status IN ('RENTED', 'RETURNED', 'EXPIRED')"))
  start_date      = Column(DateTime(timezone=True), nullable=False, default=dt.utcnow)
  till_date       = Column(DateTime(timezone=True), nullable=False)
