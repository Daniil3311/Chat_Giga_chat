import logging
import time
import uuid
from fastapi import Request
from routers.chat import router


logger = logging.getLogger(__name__)

@router.middleware("http")
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
