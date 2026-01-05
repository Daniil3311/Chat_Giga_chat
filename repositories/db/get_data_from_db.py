from sqlalchemy.orm import Session
from models.model_chat import Knowledge

def get_chat_history(db: Session, limit: int = 10):
    """
    Получаем последние N сообщений из базы
    """
    return db.query(Knowledge).order_by(Knowledge.id.desc()).limit(limit).all()[::-1]  # реверс для правильного порядка