from repositories.db.session import SessionLocal

from models.model_chat import Knowledge


class ChatRepositoryAlchemy:
    def __init__(self):
        self.session = SessionLocal()
    def save(self, data):
        try:
            self.session.add(data)
            self.session.commit()
        except Exception as e:
            raise e

    # def get(self, db):
    #     history = get_chat_history(db, limit=10)
    #     messages = [{"role": msg.role, "content": msg.content} for msg in history] # история сообщений из бд по роле и контексту
    #     # r = db.query(Knowledge).order_by(Knowledge.id.desc()).all()
    #     # result = db.execute(f"EXPLAIN {r}")
    #     # print(result.fetchall())
    #     return messages


class MessageCRUD:
    def __init__(self):
        self.session = SessionLocal()
    def save(self, user_mes, assistant_mes ):
        # изменяемо
        d = [
        Knowledge(role="user", content=user_mes),
        Knowledge(role="assistant", content=assistant_mes)]
        ch = ChatRepositoryAlchemy()
        for i in d:
            ch.save(i)

m = MessageCRUD()
m.save("!!!!!!!!!", "??????????" )