import json
from unittest import mock
import uuid
from unittest.mock import Mock
from fastapi.testclient import TestClient
from router import create_redis_client
from main import get_app
import pytest

# Get the FastAPI app from the router
app = get_app()
test_client = TestClient(app)


class TestRouter:
    def setup_method(self) -> None:
        # Create mock Redis client and user data
        self.mock_redis_client = Mock()
        self.user_id = str(uuid.uuid4())
        self.user_data = {
            "id": self.user_id,
            "name": "Test User",
            "email": "test@example.com",
        }
        # Patch RedisClient.get_redis_client to return the mock Redis client
        app.dependency_overrides[create_redis_client] = lambda: self.mock_redis_client

    def teardown_method(self) -> None:
        # Stop the patcher after each test
        app.dependency_overrides.clear()

    def test_create_user(self) -> None:
        response = test_client.post("/user", json=self.user_data)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "User created successfully"
        assert "user_id" in data

        # Ensure Redis set method was called with correct data
        self.mock_redis_client.set.assert_called_once()
        stored_user_id, stored_user_data = self.mock_redis_client.set.call_args[0]
        assert json.loads(stored_user_data)["name"] == self.user_data["name"]

    def test_get_user(self) -> None:
        # Mock Redis to return user data when queried
        self.mock_redis_client.get.return_value = json.dumps(self.user_data)

        response = test_client.get(f"/user/{self.user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == self.user_data["name"]
        assert data["email"] == self.user_data["email"]

    def test_get_user_not_found(self) -> None:
        # Mock Redis to return None for a non-existent user
        self.mock_redis_client.get.return_value = None

        response = test_client.get("/user/invalid_user_id")

        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_get_all_users(self) -> None:
        # Mock Redis keys and get methods to return multiple users
        user_id2 = str(uuid.uuid4())
        user_data2 = {
            "id": user_id2,
            "name": "Second User",
            "email": "second@example.com",
        }
        self.mock_redis_client.keys.return_value = [self.user_id, user_id2]
        self.mock_redis_client.get.side_effect = [
            json.dumps(self.user_data),
            json.dumps(user_data2),
        ]

        response = test_client.get("/users")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == self.user_data["name"]
        assert data[1]["name"] == user_data2["name"]

    def test_get_all_users_not_found(self) -> None:
        # Mock Redis keys to return an empty list
        self.mock_redis_client.keys.return_value = []

        response = test_client.get("/users")

        assert response.status_code == 404
        assert response.json() == {"detail": "There are no Users"}
