from fastapi import APIRouter, HTTPException, Depends
from redis import Redis
from database import RedisClient
from models import User
import json
import uuid

router = APIRouter()


def create_redis_client() -> Redis:
    client = RedisClient()
    return client.get_redis_client()


def get_router() -> APIRouter:
    return router


@router.post("/user")
def create_user(user: User, db: Redis = Depends(create_redis_client)) -> dict[str, str]:
    user_id = str(uuid.uuid4())
    user_dict = user.model_dump()
    user_dict["id"] = user_id

    # Store user data in Redis as a JSON string
    db.set(user_id, json.dumps(user_dict))

    return {"message": "User created successfully", "user_id": user_id}


@router.get("/user/{user_id}")
def get_user(user_id: str, db: Redis = Depends(create_redis_client)) -> User:
    user_data = db.get(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user = json.loads(user_data)  # type: ignore
    return user


@router.get("/users")
def get_all_users(db: Redis = Depends(create_redis_client)) -> list[User]:
    user_keys = db.keys()  # Get all keys
    users = []
    if user_keys:
        for key in user_keys:  # type: ignore
            user_data = db.get(key)
            user = json.loads(user_data)  # type: ignore
            users.append(user)
        return users
    else:
        raise HTTPException(status_code=404, detail="There are no Users")
