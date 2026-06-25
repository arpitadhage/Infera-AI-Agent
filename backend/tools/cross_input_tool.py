from backend.tools.groq_client import call_groq

def cross_input_reason(state):

    print("Executing: cross_input_reason")

    pdf = state["contents"].get("pdf", [])
    image = state["contents"].get("image", [])
    audio = state["contents"].get("audio", [])
    youtube = state["contents"].get("youtube", [])

    combined_text = ""

    for item in pdf:
        combined_text += item.get("text", "") + "\n"

    for item in image:
        combined_text += item.get("text", "") + "\n"

    for item in audio:
        combined_text += item.get("text", "") + "\n"

    for item in youtube:
        combined_text += item.get("text", "") + "\n"

    if not combined_text.strip():
        state["cross_input"] = "No data to compare"
        return state

    prompt = f"""
You are an expert AI reasoning engine.

Compare and analyze ALL sources below.

Task:
- Find if they talk about same topic
- Identify similarities
- Identify differences
- Give final conclusion

CONTENT:
{combined_text}
"""

    response = call_groq(prompt)

    state["cross_input"] = response

    return state