from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.giga_ch import get_giga_client, get_embedding
# from utils import should_save_message

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



class ChatRequest(BaseModel):
    message: str
    category: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # db: Session = SessionLocal()
    try:
        # 3. Получаем ответ от GigaChat
        client = get_giga_client()
        response = client.chat(req.message)
        answer = response.choices[0].message.content

        # 4. Сохраняем только полезные сообщения
        #
        # db.add(Message(role="user", content=req.message))
        # db.add(Message(role="assistant", content=answer))

        # db.commit()
        return {"answer": answer}

    finally:
        print('усе')
