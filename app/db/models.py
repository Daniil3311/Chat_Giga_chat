from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from .base import Base

class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    category = Column(String, default="faq")
    embedding = Column(Vector(1536))
