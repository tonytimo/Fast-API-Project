# routes.py
from fastapi import APIRouter


class RouteHandler:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.get("/")
        def root() -> dict[str, str]:
            return {"message": "Hello World from a class-based route"}

    def get_router(self) -> APIRouter:
        return self.router
