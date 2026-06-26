class Planner:
    """
    Creates a deterministic, ordered execution plan based on intent + file types.
    Guarantees: extraction always happens before analysis, no duplicate steps.
    """

    # Maps file type → extraction tool name
    EXTRACT_TOOL_MAP = {
        "pdf":   "extract_pdf_text",
        "image": "extract_image_text",
        "audio": "transcribe_audio",
        "docx":  "extract_docx_text",
        "code":  "extract_code",
        "txt":   "extract_text",
        "youtube": "fetch_youtube_transcript",
    }

    def create_plan(self, intent: str, file_types: list[str]) -> list[str]:
        plan: list[str] = []
        seen: set[str] = set()

        def add(step: str):
            if step not in seen:
                seen.add(step)
                plan.append(step)

        # ── 1. Extraction phase (one tool per unique file type) ──────────────
        for ft in file_types:
            tool = self.EXTRACT_TOOL_MAP.get(ft)
            if tool:
                add(tool)

        # ── 2. Analysis / reasoning phase ────────────────────────────────────
        if intent == "sentiment_analysis":
            # MUST have extracted text first
            if not plan:
                add("extract_text")          # fallback extractor
            add("analyze_sentiment")

        elif intent == "code_explanation":
            if not any(t in seen for t in ("extract_code",)):
                add("extract_code")
            add("explain_code")

        elif intent in ("cross_input_reasoning", "comparison"):
            add("build_unified_context")
            add("compare_inputs") if intent == "comparison" else add("summarize")

        elif intent == "summarization":
            add("summarize")

        elif intent == "conversation":
            add("chat_response")

        else:
            add("summarize")

        return plan