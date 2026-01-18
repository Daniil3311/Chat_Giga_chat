from fastapi import FastAPI, Response
from routers import chat
import logging
import time
import uuid
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(
    title="My API",
    version="1.0.0"
)
# # Создаем метрики (у вас уже есть, но проверьте область видимости)
# REQUEST_COUNT = Counter(
#     'myapp_requests_total',
#     'Все запросы'
# )
#
# REQUEST_TIME = Histogram(
#     'myapp_request_time_seconds',
#     'Время выполнения запросов',
#     buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
# )
#
# # Дополнительные метрики для мониторинга
# CHAT_ERRORS = Counter(
#     'myapp_chat_errors_total',
#     'Ошибки в чате'
# )
#
# CHAT_DURATION = Histogram(
#     'myapp_chat_duration_seconds',
#     'Длительность обработки чата'
# )

logger = logging.getLogger(__name__)

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(f"Начало запроса: {request.method} {request.url.path}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Client: {request.client}")
    request.state.request_id = request_id

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        f"Конец запроса: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {duration:.2f}ms"
    )
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time"] = str(duration)

    print(f"[{request_id}] {request.method} {request.url} {duration:.4f}s")

    return response

@app.get("/hello")
async def hello():
    return {"msg": "hi"}


from fastapi.responses import StreamingResponse

def file_generator(num):
    for i in range(num):
        yield f"{i}\n"

@app.get("/export/{num}")
def export(num:int):
    return StreamingResponse(file_generator(num), media_type="text/plain")

from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        data = await ws.receive_text()
        await ws.send_text(f"echo: {data}")

app.include_router(chat.router)
