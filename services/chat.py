from fastapi import Depends
from sqlalchemy.orm import Session
from repositories.giga_chat_api.settings_gigachat import giga
from sсhemas.chat import ChatRequest,ChatResponse
from repositories.db.chat import ChatRepositoryAlchemy, get_db
from abc import ABC, abstractmethod
from typing import Optional

class IChatRepository(ABC):
    @abstractmethod
    def get(self, db: Session):
        pass

    @abstractmethod
    def save(self, user_mes: str, assistant_mes: str, db: Session):
        pass


class ILLMService(ABC):
    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass


class ChatLLMGigachat:
    # def __init__(self):
    #     # self.repository = repository
    #     # self.service = ILLMService()

    def save_and_response(self, req: ChatRequest, db: Session):
        try:
            chat_repo = ChatRepositoryAlchemy()
            # messages = chat_repo.get(db)
            messages = chat_repo.get(db)
            messages.append({"role": "user", "content": req.message})
            response = giga.chat({"messages": messages})

            answer = response.choices[0].message.content
            chat_repo.save(req.message, answer, db)
        except Exception as error:
            raise error

        return {"answer": answer}


# class LLMService:
#     def __init__(self, llm_service):
#         self.llm_service = llm_service
#
#     def chat(self, data: dict):
#         response = self.llm_service(data)


# class ChatLLM:
#     def __init__(self):
#         self.repository = ChatRepository()
#         self.service = LLMService(giga)
#         self.session = Session()
#
#     def get(self):
#         return self.repository.get()