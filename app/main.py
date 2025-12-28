from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.db.models import Knowledge
from .db.session import SessionLocal
from app.giga_ch import giga, get_chat_history

app = FastAPI()



class ChatRequest(BaseModel):
    message: str
    category: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    db = SessionLocal()
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
        return {"answer": answer}
    except Exception as e:
        db.rollback()
        # Возвращаем ошибку HTTP
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
