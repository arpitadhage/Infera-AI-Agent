import json
from backend.tools.groq_client import call_groq


def analyze_sentiment(state):
    print("Executing: sentiment_analysis")

    text = ""

    # collect all available text
    for item in state["contents"]["pdf"]:
        text += item.get("text", "") + "\n"

    for item in state["contents"]["image"]:
        text += item.get("text", "") + "\n"

    for item in state["contents"]["audio"]:
        text += item.get("text", "") + "\n"

    for item in state["contents"]["docx"]:
        text += item.get("text", "") + "\n"

    for item in state["contents"]["text"]:
        text += item.get("text", "") + "\n"

    if not text.strip():
        state["sentiment"] = {
            "label": "neutral",
            "confidence": 0.0,
            "reason": "No text found"
        }
        return state

    prompt = f"""
Analyze the sentiment of the following text.

Return STRICT JSON ONLY:

{{
  "label": "positive | negative | neutral",
  "confidence": 0-1,
  "reason": "one line explanation"
}}

TEXT:
{text}
"""

    response = call_groq(prompt)

    try:
        state["sentiment"] = json.loads(response)
    except:
        state["sentiment"] = {
            "label": "neutral",
            "confidence": 0.5,
            "reason": "Parsing failed"
        }

    return state