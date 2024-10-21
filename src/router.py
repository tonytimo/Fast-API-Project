# routes.py
import json
from fastapi import APIRouter


def _setup() -> list[dict]:
    with open("data.json", "r") as f:
        json_str = f.read()
    data = json.loads(json_str).get("users")
    return data

router = APIRouter()
data = _setup()


@router.get("/users")
def get_users() -> list[dict[str, str]]:
    return data

@router.get("/users/{id}")
def get_user(id: str) -> dict[str, str]:
    for user in data:
        if id == user.get("id"):
            return user
    
    return {"message": f"there is no such user with id:{id}"}

    # @self.router.post("/user")
    # def add_user() -> dict[str, str]:
    #     return {"message": "Hello World from a class-based route"}


def get_router() -> APIRouter:
    return router
