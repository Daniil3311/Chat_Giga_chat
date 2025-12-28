from typing import List

from gigachat import GigaChat
import os
import logging

from sqlalchemy.orm import Session

from app.db.models import Knowledge

# logger = logging.getLogger(__name__)
#
# # БЕЗОПАСНОСТЬ: читаем API ключ из переменной окружения
# api_key = os.getenv("GIGACHAT_API_KEY")
#
giga = GigaChat(
        credentials=os.getenv("GIGACHAT_API_KEY"),
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False  # для локальной разработки
    )


def get_chat_history(db: Session, limit: int = 10):
    """
    Получаем последние N сообщений из базы
    """
    return db.query(Knowledge).order_by(Knowledge.id.desc()).limit(limit).all()[::-1]  # реверс для правильного порядка