#from backend.tools.groq_client import generate
from backend.tools.groq_client import call_groq


def summarize(state):

    print("Executing: summarize")

    all_text = ""
    

    # PDF text
    for item in state["contents"]["pdf"]:
        all_text += item.get("text", "") + "\n"

    # Image OCR text
    for item in state["contents"]["image"]:
        all_text += item.get("text", "") + "\n"

    # Audio transcript
    for item in state["contents"]["audio"]:
        all_text += item.get("text", "") + "\n"

    # YouTube transcript
    for item in state["contents"]["youtube"]:
        all_text += item.get("text", "") + "\n"

    # URL-based text (optional future use)
    for item in state.get("contents", {}).get("urls", []):
        all_text += str(item) + "\n"

    MAX_CHARS = 8000

    all_text = all_text[:MAX_CHARS]

    if not all_text.strip():
        state["summary"] = "No content found to summarize"
        return state

    prompt = f"""
You are an expert AI assistant.

Your task is to summarize the following multimodal content.

Return strictly in this format:

1. One line summary
2. 3 bullet points
3. Detailed explanation
4. Cross-Input Relationship:
   - Connected / Partially Connected / Not Related
   - Reasoning

CONTENT:
{all_text}
"""

    try:
        summary = call_groq(prompt)
        state["summary"] = summary

    except Exception as e:
        state["summary"] = f"Summarization failed: {str(e)}"

    return state