import re


def detect_urls(state):

    all_text = ""
    for pdf in state["contents"]["pdf"]:
        all_text += pdf["text"] + "\n"

    for image in state["contents"]["image"]:
        all_text += image["text"] + "\n"

    for audio in state["contents"]["audio"]:
        all_text += audio["text"] + "\n"

    for yt in state["contents"]["youtube"]:
        all_text += yt["text"] + "\n"

    urls = re.findall(
        r'https?://[^\s]+',
        all_text
    )

    state["urls"] = urls

    return state


