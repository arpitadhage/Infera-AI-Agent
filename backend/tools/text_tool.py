def extract_text(state):

    file_path = state["file_path"]

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    state["contents"]["text"] = [{
        "text": text
    }]

    return state