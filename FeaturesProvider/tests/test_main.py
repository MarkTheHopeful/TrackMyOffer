import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_home_route(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


@pytest.mark.parametrize(
    "mock_return,payload,expected_status,expected_response",
    [
        ("Hello, John!", {"name": "John"}, 200, {"message": "Hello, John!"}),
        (None, {"name": "John"}, 503, {"detail": "AI service is currently unavailable"}),
        (None, {}, 400, {"detail": "Name is required"}),
    ],
)
def test_greet_route(
    client: TestClient,
    mock_return: str | None,
    payload: dict[str, str],
    expected_status: int,
    expected_response: dict[str, str],
) -> None:
    with patch("main.request_model", return_value=mock_return):
        response = client.post("/greet", json=payload)
        assert response.status_code == expected_status
        assert response.json() == expected_response
