import os

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from app.db.models import Knowledge
from app.db.session import SessionLocal
from app.giga_ch import giga, get_chat_history
import redis
import json

# r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"),
#                 port=int(os.getenv("REDIS_PORT", 6379)),
#                 db=0)

app = FastAPI()



class ChatRequest(BaseModel):
    message: str
    category: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    db = SessionLocal()
    last_message = req.message[-1]
    # cached = r.get(last_message)
    # if cached:
    #     return {"message": cached.decode("utf-8")}

    try:
        # 3. Получаем ответ от GigaChat


        history = get_chat_history(db, limit=10)
        messages = [{"role": msg.role, "content": msg.content} for msg in history]
        messages.append({"role": "user", "content": req.message})

        response = giga.chat({"messages": messages})
        answer = response.choices[0].message.content

        db.add(Knowledge(role="user", content=req.message))
        db.add(Knowledge(role="assistant", content=answer))

        db.commit()
        # r.setex(req.message, 600, answer)
        return {"answer": answer}
    except Exception as e:
        db.rollback()
        # Возвращаем ошибку HTTP
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
