from contextlib import contextmanager
import time

from fastapi import APIRouter, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from prometheus_client import Counter, Histogram, generate_latest
from repositories.db.chat import ChatRepositoryAlchemy
from repositories.db.session import get_db
from services.chat import ChatLLMGigachat
from services.ws_manager import ConnectionManager
from sсhemas.chat import ChatRequest,ChatResponse


router = APIRouter(prefix='/base')

REQUEST_COUNT = Counter(
    'myapp_requests_total',
    'Все запросы'
)

REQUEST_TIME = Histogram(
    'myapp_request_time_seconds',
    'Время выполнения запросов',
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

# Дополнительные метрики для мониторинга
CHAT_ERRORS = Counter(
    'myapp_chat_errors_total',
    'Ошибки в чате'
)

CHAT_DURATION = Histogram(
    'myapp_chat_duration_seconds',
    'Длительность обработки чата'
)


@contextmanager
def track_request_metrics():
    """Контекстный менеджер для отслеживания метрик запроса"""
    start_time = time.time()
    try:
        yield
    except Exception:
        CHAT_ERRORS.inc()
        raise
    finally:
        duration = time.time() - start_time
        REQUEST_TIME.observe(duration)


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    REQUEST_COUNT.inc()

    with track_request_metrics():
        with CHAT_DURATION.time():
            ch = ChatLLMGigachat()
            save_ch = ch.save_and_response1(req, db)

    return save_ch


manager = ConnectionManager()

@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)