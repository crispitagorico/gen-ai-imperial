"""
Sentiment analysis — FinBERT wrapper.

Returns sentiment scores for a list of texts.
"""

from __future__ import annotations

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


_PIPELINE = None


def _get_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        model_name = "ProsusAI/finbert"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _PIPELINE = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            truncation=True,
            max_length=512,
        )
    return _PIPELINE


def analyze_sentiment(texts: list[str]) -> list[dict]:
    """
    Score each text as positive / negative / neutral.

    Returns list of {"text": ..., "label": ..., "score": ...}.
    """
    if not texts:
        return []
    pipe = _get_pipeline()
    results = pipe(texts, batch_size=16)
    return [
        {
            "text": t[:120],
            "label": r["label"],
            "score": round(r["score"], 4),
        }
        for t, r in zip(texts, results)
    ]
