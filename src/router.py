# routes.py
import json
from fastapi import APIRouter


def _setup() -> dict[str, list[dict[str,str|int]]]:
    with open(file="data.json", mode="r", encoding="utf-8") as f:
        json_str = f.read()
    user_list = json.loads(json_str)
    return user_list

router = APIRouter()
data = _setup()


@router.get("/users")
def get_users() -> list[dict[str, str|int]]:
    return data.get("users") # type: ignore

@router.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, str|int]:
    for user in data.get("users"): # type: ignore
        if user_id == user.get("user_id"):
            return user
    return {"message": f"there is no such user with id:{id}"}

@router.post("/user")
def add_user(name: str) -> dict[str, str|int]:
    user_id = data.get("users")[-1].get("user_id")+1 # type: ignore
    data["users"].append({"user_id": user_id, "name": name})
    with open(file="data.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    return {"user_id": user_id, "name": name}


def get_router() -> APIRouter:
    return router
