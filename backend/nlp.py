from transformers import pipeline

# Lightweight, CPU/GPU friendly model
summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small"
)

def summarize_text(text: str) -> str:
    text = text.strip().replace("\n", " ")
    text = text[:2000]  # safety limit

    result = summarizer(
        text,
        max_length=160,
        min_length=60,
        do_sample=False
    )

    return result[0]["summary_text"]

def answer_question(context: str, question: str) -> str:
    context = context.strip().replace("\n", " ")
    context = context[:2000]

    prompt = (
        "Read the content below and answer the question by explaining the MAIN IDEA "
        "in your own words. Do NOT repeat lines or quotes.\n\n"
        f"Content:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        "Answer:"
    )

    result = summarizer(
        prompt,
        max_length=80,
        min_length=40,
        do_sample=False
    )

    return result[0]["summary_text"]
