from fastapi import APIRouter, HTTPException
from database import RedisClient
from pydantic import BaseModel
import json
import uuid

router = APIRouter()
redis_client = RedisClient().redis_client


def get_router() -> APIRouter:
    return router


# User model
class User(BaseModel):
    name: str
    email: str


@router.post("/user")
def create_user(user: User) -> dict[str, str]:
    user_id = str(uuid.uuid4())
    user_dict = user.dict()
    user_dict["id"] = user_id

    # Store user data in Redis as a JSON string
    redis_client.set(user_id, json.dumps(user_dict))

    return {"message": "User created successfully", "user_id": user_id}


@router.get("/user/{user_id}")
def get_user(user_id: str) -> User:
    user_data = redis_client.get(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user = json.loads(user_data)  # type: ignore
    return user


@router.get("/users")
def get_all_users() -> list[User]:
    user_keys = redis_client.keys()  # Get all keys
    users = []
    if user_keys:
        for key in user_keys:  # type: ignore
            user_data = redis_client.get(key)
            user = json.loads(user_data)  # type: ignore
            users.append(user)
        return users
    else:
        raise HTTPException(status_code=404, detail="There are no Users")
