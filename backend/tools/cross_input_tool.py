from backend.tools.groq_client import call_groq

def cross_input_reason(state):

    texts = state["contents"]

    all_text = ""

    for k in texts:
        for item in texts[k]:
            all_text += item.get("text", "") + "\n"

    if not all_text.strip():
        state["cross_input"] = {
            "relation": "no_data",
            "reason": "No content found"
        }
        return state

    prompt = f"""
You are a cross-input reasoning system.

Analyze if all inputs are related or not.

Rules:
1. If topics are same → mark "CONNECTED"
2. If partially related → "PARTIALLY_CONNECTED"
3. If different → "NOT_CONNECTED"

Also explain:
- main topics
- similarity score (0-100)
- reasoning

CONTENT:
{all_text}
"""

    result = call_groq(prompt)

    state["cross_input"] = result

    return state