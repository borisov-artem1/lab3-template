from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.settings import get_db_url


engine = create_engine(
    url = get_db_url()
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
