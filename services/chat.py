from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.giga_chat_api.settings_gigachat import giga
from repositories.redis.hisrory_chat_redis import HistoryRedis
from sсhemas.chat import ChatRequest
from repositories.db.chat import ChatRepositoryAlchemy


class ChatLLMGigachat:
    def __init__(self):
        self.chat_repo_res = HistoryRedis()
        # self.chat_repo_pos = MessageCRUD
        # self.service = ILLMService()
        self.chat_repo_pos = ChatRepositoryAlchemy()

    def save_and_response1(self, req: ChatRequest, db: Session):
        try:
            # История из Redis
            messages_re = self.chat_repo_res.get_chat_history(db)
            if not messages_re:
                raise HTTPException(status_code=404, detail="Data not found")
            else:
                messages_re.append({"role": "user", "content": req.message})

            response = giga.chat({"messages": messages_re})
            if not response:
                raise HTTPException(status_code=404, detail="Data not found")

            answer = response.choices[0].message.content
            # сохранение в Postgres
            self.chat_repo_pos.save(req.message, answer, db)
            # сохранение в Redis
            self.chat_repo_res.add_message(req.message, answer)
        except Exception as error:
            raise error

        return {"answer": answer}


    def save_and_response(self,req: ChatRequest, db: Session):
        try:
            chat_repo = ChatRepositoryAlchemy()
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



        #     chat_repo = ChatRepositoryAlchemy()
        #     messages = chat_repo.get(db)
        #     messages.append({"role": "user", "content": req.message})
        #     response = giga.chat({"messages": messages})
        #
        #     answer = response.choices[0].message.content
        #     chat_repo.save(req.message, answer, db)
        # except Exception as error:
        #     raise error
        #
        # return {"answer": answer}