from sqlalchemy import Column, Integer, String, Text
from repositories.db.base import Base

class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    role = Column(String, index=True)
    # session = Column()
    # category = Column(String, default="faq")
    # embedding = Column(Vector(1536))

