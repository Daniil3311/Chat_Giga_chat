import json
import logging

import redis
from sqlalchemy.orm import Session

from repositories.db.chat import ChatRepositoryAlchemy

REDIS_TTL = 56400  # 1 день в секундах

# Подключение к Redis
# redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
logging.basicConfig(filename="chat.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class HistoryRedis:
    def __init__(self, host="localhost", port=6380, db=0):
            self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.key = "chat:history"

            if self.redis.ping():
                self.is_available = True
                logger.info(f"Redis подключен успешно к {host}:{port}")
            else:
                raise Exception("Redis не ответил на PING")

    # если в redis есть то, выдает из него если нет то postgres и сохраняет в redis
    def get_chat_history(self, db: Session):
        history_json = self.redis.get(self.key)

        logger.info("Берём историю из Redis:")

        logger.info(history_json)
        if history_json:
            return json.loads(history_json)
            # Если Redis пустой, достаём из Postgres
        history_postgres = ChatRepositoryAlchemy()
        his_pos = history_postgres.get(db)
        # Сохраняем в Redis на 1 день
        self.redis.set(self.key, json.dumps(his_pos), ex=REDIS_TTL)
        return his_pos
    
    def get_history(self):
            data = self.redis.get(self.key)
            if data:
                return json.loads(data)
            return []


    def add_message(self, req, content):
        history = self.get_history()
        history.append({"role": 'user', "content": req})
        history.append({"role": 'assistant', "content": content})
        self.redis.set(self.key, json.dumps(history), ex=REDIS_TTL)

