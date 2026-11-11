
import re

from backend.portfolio_data import PORTFOLIO_CONTEXT


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can",
    "could", "did", "do", "does", "for", "from", "give",
    "has", "have", "he", "her", "his", "how", "i", "in",
    "is", "it", "me", "my", "of", "on", "or", "please",
    "tell", "that", "the", "their", "them", "there", "this",
    "to", "was", "what", "when", "where", "which", "who",
    "why", "will", "with", "would", "you", "your",
    "balaram", "chintala", "explain", "describe", "about",
    "project", "projects", "information", "details",
}


def tokenize(text: str) -> set[str]:
    """Convert text into searchable lowercase words."""
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    }


def split_portfolio_sections() -> list[dict[str, str]]:
    """Split the portfolio context using its Markdown headings."""
    parts = re.split(
        r"(?m)^##\s+(.+?)\s*$",
        PORTFOLIO_CONTEXT,
    )

    sections = []

    # Content before the first heading, if any.
    if parts[0].strip():
        sections.append({
            "title": "INTRODUCTION",
            "content": parts[0].strip(),
        })

    # Remaining items alternate between heading and section content.
    for index in range(1, len(parts), 2):
        title = parts[index].strip()
        content = parts[index + 1].strip()

        if content:
            sections.append({
                "title": title,
                "content": f"## {title}\n{content}",
            })

    return sections


PORTFOLIO_SECTIONS = split_portfolio_sections()



def retrieve_portfolio_context(
    question: str,
    max_sections: int = 3,
) -> str:
    """Return relevant portfolio sections for a question."""

    normalized_question = question.lower().strip()

    # Return all portfolio sections for broad profile questions.
    broad_questions = [
        "all about balaram",
        "everything about balaram",
        "tell me about balaram",
        "who is balaram",
        "introduce balaram",
        "balaram's profile",
        "balaram profile",
        "describe balaram",
        "who is he",
        "about him",
        "introduce him",
        "describe him",
        "his profile",
        "his background",
        "who are you",
        "about you",
    ]

    if any(phrase in normalized_question for phrase in broad_questions):
        return "\n\n".join(
            section["content"] for section in PORTFOLIO_SECTIONS
        )


    project_phrases = [
        "what projects",
        "which projects",
        "projects has balaram worked on",
        "balaram's projects",
        "list the projects",
        "all projects",
        "any projects",
        "any project",
        "his projects",
        "projects he",
        "projects did",
        "projects does",
        "his work",
    ]

    if any(
        phrase in question.lower()
        for phrase in project_phrases
    ):
        project_sections = [
            section["content"]
            for section in PORTFOLIO_SECTIONS
            if any(
                word in (
                    section["title"] + " " + section["content"]
                ).lower()
                for word in [
                    "zywave",
                    "quantivrisk",
                    "msig",
                    "sql rag agent",
                    "portfolio ai assistant",
                ]
            )
        ]

        if project_sections:
            return "\n\n".join(project_sections)

    # Vague questions with no searchable words fall back to the profile,
    # because every question on this site is about Balaram.
    profile_context = "\n\n".join(
        section["content"]
        for section in PORTFOLIO_SECTIONS
        if section["title"] == "PROFILE"
    )

    query_words = tokenize(question)

    if not query_words:
        return profile_context

    scored_sections = []

    for section in PORTFOLIO_SECTIONS:
        section_words = tokenize(section["content"])
        overlap = query_words & section_words

        if not overlap:
            continue

        # Give matching heading terms extra importance.
        heading_words = tokenize(section["title"])
        heading_matches = query_words & heading_words

        score = len(overlap) + 2 * len(heading_matches)

        scored_sections.append(
            (score, section["content"])
        )

    scored_sections.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    selected = [
        content
        for score, content in scored_sections[:max_sections]
    ]

    return "\n\n".join(selected) or profile_context
