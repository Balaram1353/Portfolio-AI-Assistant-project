import pytest

from backend.portfolio_retriever import retrieve_portfolio_context


@pytest.mark.parametrize(
    "question",
    ["who is he", "Who is he?", "tell me about him", "what is his profile"],
)
def test_pronoun_questions_return_profile(question):
    context = retrieve_portfolio_context(question)

    assert "Balaram Naidu Chintala" in context


@pytest.mark.parametrize(
    "question",
    [
        "does he contributed to any projects if yes what are they",
        "what are his projects",
        "which projects he worked on",
    ],
)
def test_project_questions_return_all_projects(question):
    context = retrieve_portfolio_context(question)

    for heading in [
        "## CLIENT PROJECT 1: ZYWAVE",
        "## CLIENT PROJECT 2: QUANTIVRISK",
        "## CLIENT PROJECT 3: MSIG",
        "## PERSONAL PROJECT 1: SQL RAG AGENT",
        "## PERSONAL PROJECT 2: PORTFOLIO AI ASSISTANT",
    ]:
        assert heading in context


@pytest.mark.parametrize("question", ["is", "xyzzy qwerty"])
def test_unmatched_questions_fall_back_to_profile(question):
    context = retrieve_portfolio_context(question)

    assert "## PROFILE" in context
