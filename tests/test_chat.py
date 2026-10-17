
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from backend import main

client = TestClient(main.app)


class FakeLLM:
    """Simulate a successful model response."""

    def invoke(self, question):
        return SimpleNamespace(
            content=f"Test answer for: {question}",
            response_metadata={},
        )


class FailingLLM:
    """Simulate an NVIDIA API failure."""

    def invoke(self, question):
        raise RuntimeError("Simulated model failure")


QUESTIONS = [
    "What is machine learning? Explain in 3 sentences.",
    "Explain the difference between RAG and fine-tuning.",
    "What skills are useful for a data scientist?",
]


@pytest.mark.parametrize("question", QUESTIONS)
def test_chat_returns_valid_answer(question, monkeypatch):
    monkeypatch.setattr(main, "llm", FakeLLM())

    response = client.post("/chat", json={"question": question})

    assert response.status_code == 200
    data = response.json()

    assert data["question"] == question
    assert isinstance(data["answer"], str)
    assert data["answer"].strip() != ""
    assert "error" not in data


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Portfolio AI Chatbot API is running!"
    )


def test_chat_missing_question():
    response = client.post("/chat", json={})

    assert response.status_code == 422


def test_chat_wrong_question_type():
    response = client.post("/chat", json={"question": 123})

    assert response.status_code == 422


def test_chat_empty_question():
    response = client.post(
        "/chat",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_chat_model_error(monkeypatch):
    monkeypatch.setattr(main, "llm", FailingLLM())

    response = client.post(
        "/chat",
        json={"question": "Test error handling"}
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "The AI model request failed. "
        "Please try again. Check the backend terminal for details."
    )

def test_chat_whitespace_question():
    response = client.post(
        "/chat",
        json={"question": "     "}
    )

    assert response.status_code == 422