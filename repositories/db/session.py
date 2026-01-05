import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
db_name = os.getenv("DATABASE_NAME")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "chatdb_giga")
POSTGRES_HOST = "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()