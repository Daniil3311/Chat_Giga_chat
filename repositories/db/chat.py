from abc import ABC, abstractmethod

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from .session import SessionLocal, get_db
from models.model_chat import Knowledge
from .get_data_from_db import get_chat_history


class ChatStorage(ABC):
    @abstractmethod
    def save(self, user_mes, assistant_mes, db):
        pass

    @abstractmethod
    def get(self, db):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def path(self):
        pass

class ChatRepositoryAlchemy(ChatStorage):

    def save(self, user_mes, assistant_mes, db):
        try:
            db.add(Knowledge(role="user", content=user_mes))
            db.add(Knowledge(role="assistant", content=assistant_mes))
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get(self, db):
        history = get_chat_history(db, limit=10)
        messages = [{"role": msg.role, "content": msg.content} for msg in history] # история сообщений из бд по роле и контексту
        return messages

    def delete(self):
        pass

    def put(self):
        pass

    def path(self):
        pass