def build_unified_context(state):

    context_parts = []

    # PDF
    for item in state["contents"].get("pdf", []):
        context_parts.append("PDF:\n" + item.get("text", ""))

    # Image
    for item in state["contents"].get("image", []):
        context_parts.append("IMAGE:\n" + item.get("text", ""))

    # Audio
    for item in state["contents"].get("audio", []):
        context_parts.append("AUDIO:\n" + item.get("text", ""))

    # Docx
    for item in state["contents"].get("docx", []):
        context_parts.append("DOCX:\n" + item.get("text", ""))

    # Text
    for item in state["contents"].get("text", []):
        context_parts.append("TEXT:\n" + item.get("text", ""))

    # Code
    for item in state["contents"].get("code", []):
        context_parts.append("CODE:\n" + item.get("text", ""))

    state["unified_context"] = "\n\n".join(context_parts)

    return state