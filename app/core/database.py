from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import DATABASE_URL

class Base(DeclarativeBase):
    pass
engine = create_engine(DATABASE_URL,echo=True)
SessionLocal= sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)