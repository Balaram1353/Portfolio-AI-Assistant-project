
import os
from types import SimpleNamespace
from unittest.mock import patch

# Set a placeholder key before importing the application.
# Tests will mock the model, so no real NVIDIA API call is made.
os.environ.setdefault("NVIDIA_API_KEY", "test-api-key")

from fastapi.testclient import TestClient
from backend import main


client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Portfolio AI Chatbot API is running!"
    )


def test_empty_question_is_rejected():
    response = client.post(
        "/chat",
        json={"question": "   "},
    )

    assert response.status_code == 422


def test_missing_question_is_rejected():
    response = client.post("/chat", json={})

    assert response.status_code == 422



def test_chat_returns_an_answer():
    fake_response = SimpleNamespace(
        content="Balaram is an Associate Data Scientist.",
        response_metadata={"finish_reason": "stop"},
    )

    fake_llm = SimpleNamespace(
        invoke=lambda prompt: fake_response
    )

    with (
        patch.object(
            main,
            "retrieve_portfolio_context",
            return_value="Balaram is an Associate Data Scientist.",
        ),
        patch.object(main, "llm", fake_llm),
    ):
        response = client.post(
            "/chat",
            json={
                "question": "Who is Balaram? Give me a short introduction."
            },
        )

    assert response.status_code == 200

    data = response.json()
    assert data["question"] == (
        "Who is Balaram? Give me a short introduction."
    )
    assert data["answer"]
    assert "Balaram" in data["answer"]




def test_model_failure_returns_502():
    def fail_invoke(prompt):
        raise RuntimeError("Simulated model failure")

    fake_llm = SimpleNamespace(invoke=fail_invoke)

    with (
        patch.object(
            main,
            "retrieve_portfolio_context",
            return_value="Balaram's portfolio information.",
        ),
        patch.object(main, "llm", fake_llm),
    ):
        response = client.post(
            "/chat",
            json={"question": "Who is Balaram?"},
        )

    assert response.status_code == 502
    assert "AI model request failed" in response.json()["detail"]
