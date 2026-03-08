"""Sentiment Analyzer Flask Application."""
from flask import Flask
from transformers import pipeline

app = Flask(__name__)

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


@app.route("/analyze/<text>", methods=["GET"])
def analyze_review(text):
    """Analyze sentiment of the given text."""
    result = sentiment_pipeline(text)
    label = result[0]['label'].lower()
    if label == "positive":
        sentiment = "positive"
    elif label == "negative":
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {"sentiment": sentiment}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
