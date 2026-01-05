from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from repositories.db.chat import ChatRepositoryAlchemy
from repositories.db.session import get_db
from services.chat import ChatLLMGigachat
from sсhemas.chat import ChatRequest,ChatResponse


router = APIRouter(prefix='/base')

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    ch = ChatLLMGigachat()
    save_ch = ch.save_and_response(req, db)
    return save_ch
