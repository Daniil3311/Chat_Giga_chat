from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    category: str

class ChatResponse(BaseModel):
    answer: str