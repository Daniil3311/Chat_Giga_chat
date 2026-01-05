from fastapi import FastAPI, APIRouter, Header, Cookie
from routers import chat
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="My API",
    version="1.0.0"
)
@app.get("/hello")
async def hello():
    return {"msg": "hi"}

Instrumentator().instrument(app).expose(app)
app.include_router(chat.router)
# Instrumentator(
#     should_ignore_untemplated=True,
#     should_group_status_codes=False,
#     should_respect_env_var=True,
# ).instrument(app).expose(app)

instrumentator = Instrumentator(
    should_ignore_untemplated=True,
    should_group_status_codes=False,
    should_respect_env_var=True,
)

instrumentator.instrument(app)
instrumentator.expose(app)

print("Prometheus metrics enabled:", instrumentator.enabled)