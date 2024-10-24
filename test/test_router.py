import pytest
from fastapi.testclient import TestClient
from ..src.main import get_app


class TestRouter:
    @classmethod
    def setup_class(cls) -> None:
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.client = TestClient(get_app())

    # def test_get_users(self) -> None:
    #     response = self.client.get("/users")
    #     assert response.status_code == 200
    #     assert response.json() == [
    #         {"user_id": 1, "name": "Joe"},
    #         {"user_id": 2, "name": "Ron"},
    #         {"user_id": 3, "name": "Dan"},
    #         {"user_id": 4, "name": "John"},
    #         {"user_id": 5, "name": "Don"},
    #     ]

    # def test_get_user(self) -> None:
    #     response = self.client.get("/users/1")
    #     assert response.status_code == 200
    #     assert response.json() == {"user_id": 1, "name": "Joe"}
