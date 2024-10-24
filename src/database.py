import redis


class RedisClient:
    def __init__(self) -> None:
        # Initialize Redis client
        self.redis_client = redis.Redis(
            host="localhost", port=6379, db=0, decode_responses=True
        )
