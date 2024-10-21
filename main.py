from fastapi import FastAPI
from router import RouteHandler


def main() -> FastAPI:
    app = FastAPI()
    route_handler = RouteHandler()

    app.include_router(route_handler.get_router())
    return app
