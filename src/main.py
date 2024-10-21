from fastapi import FastAPI
from router import get_router


def main() -> FastAPI:
    app = FastAPI()
    app.include_router(get_router())
    return app
