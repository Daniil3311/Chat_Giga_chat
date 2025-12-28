import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv("DATABASE_NAME")
DATABASE_URL = f"postgresql+psycopg2://postgres:postgres@localhost:5432/chatdb_giga"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)