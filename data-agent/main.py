from fastapi import FastAPI

from app.api.routers.chat_router import chat_router
from app.core.lifespan import lifespan
from app.core.middleware import RequestIDMiddleware

app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)

app.add_middleware(RequestIDMiddleware)


# 断点调试
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)

