from transformers import pipeline

# Load a lightweight summarization model
# t5-small is fast and works on CPU/MacBook Air
summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small"
)

def generate_summary(text):
    """
    Generates a short summary from text.
    This is extractive-style summarization (not deep reasoning).
    """

    # Avoid processing extremely small inputs
    if len(text) < 50:
        return text

    # Generate summary
    summary = summarizer(
        text,
        max_new_tokens=120,  # length of summary
        min_length=40,       # minimum summary length
        do_sample=False      # deterministic output
    )

    return summary[0]["summary_text"]
