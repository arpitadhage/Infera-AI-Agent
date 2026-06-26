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

    # URL-based text 
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


You are an expert multimodal AI agent.

You will receive extracted content from multiple sources:

- PDF text
- Image OCR text
- Audio transcript
- YouTube transcript
- Code snippets
- User query

Your job is to:

1. Understand user intent (even if unclear)
2. Decide best response type:
   - Summarization
   - Sentiment analysis
   - Code explanation
   - Question answering
   - Conversation
3. If multiple inputs exist:
   - Analyze relationship between them

4. Cross-Input Relationship:
   - Connected / Partially Connected / Not Related
   - Explain reasoning clearly

5. Always respond in this format:

Response:
 Final Answer 

Analysis:
- Type of task detected
- Reasoning
- Cross-input relationship (if applicable)
CONTENT:
{all_text}
"""

    try:
        summary = call_groq(prompt)
        state["summary"] = summary

    except Exception as e:
        state["summary"] = f"Summarization failed: {str(e)}"

    return state