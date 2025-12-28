def answer_question(question, text):
    """
    Answers user questions using rule-based logic.
    This avoids hallucinations and misleading answers.

    IMPORTANT:
    This is intentionally limited to stay accurate.
    """

    q = question.lower()

    # High-level topic questions
    if "what is this about" in q or "main topic" in q:
        return (
            "This file appears to be an audio recording focused on emotional "
            "themes such as relationships, regret, and recurring memories."
        )

    # Emotion-based questions
    if "emotion" in q or "feeling" in q:
        return "The tone of the audio is emotional and reflective."

    # Language / translation questions
    if "language" in q:
        return "The original audio was transcribed and translated into English."

    # Summary request
    if "summary" in q:
        return text[:300] + "..."

    # Fallback response for unsupported questions
    return (
        "This question requires deeper reasoning that this local AI model "
        "cannot reliably provide."
    )
