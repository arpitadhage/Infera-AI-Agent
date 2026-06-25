import json
from backend.tools.groq_client import call_groq


def extract_code(state):
    file_path = state["file_path"]

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    state["contents"]["code"] = [{
        "text": code
    }]

    return state

def explain_code(state):

    print("Executing: code_explanation")

    code_chunks = state["contents"].get("code", [])

    code = "\n".join([c.get("text", "") for c in code_chunks])

    if not code.strip():
        state["code_explanation"] = {
            "explanation": "No code found",
            "bugs": [],
            "time_complexity": "Unknown"
        }
        return state

    prompt = f"""
Return STRICT JSON ONLY.
NO markdown.
NO ```json.
NO explanation text.

Format:
{{
  "explanation": "...",
  "bugs": [],
  "time_complexity": "..."
}}

Code:
{code}
"""

    response = call_groq(prompt)

    try:
        state["code_explanation"] = json.loads(response)
    except:
        state["code_explanation"] = {
            "explanation": response,
            "bugs": [],
            "time_complexity": "unknown"
        }

    return state