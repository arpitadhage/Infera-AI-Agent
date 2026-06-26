from backend.tools.tools import (
    extract_pdf_text, extract_image_text, transcribe_audio,
    extract_docx_text, extract_code, extract_text,
    fetch_youtube_transcript, analyze_sentiment, explain_code,
    summarize, build_unified_context, compare_inputs, chat_response,
)

TOOL_REGISTRY = {
    "extract_pdf_text":         extract_pdf_text,
    "extract_image_text":       extract_image_text,
    "transcribe_audio":         transcribe_audio,
    "extract_docx_text":        extract_docx_text,
    "extract_code":             extract_code,
    "extract_text":             extract_text,
    "fetch_youtube_transcript": fetch_youtube_transcript,
    "analyze_sentiment":        analyze_sentiment,
    "explain_code":             explain_code,
    "summarize":                summarize,
    "build_unified_context":    build_unified_context,
    "compare_inputs":           compare_inputs,
    "chat_response":            chat_response,
}


class Executor:
    """
    Executes each tool in the plan exactly once, in order.
    - No duplicate execution (set guard)
    - LLM errors are surfaced cleanly to the user (not swallowed)
    - Extraction errors are logged but don't stop the pipeline
    """

    # Tools that call the LLM — errors here should surface to the user
    LLM_TOOLS = {
        "analyze_sentiment", "explain_code", "summarize",
        "compare_inputs", "chat_response",
    }

    def execute(self, plan: list, state: dict) -> tuple:
        logs = []
        executed = set()

        for step in plan:
            # ── Duplicate guard ──────────────────────────────────────────────
            if step in executed:
                logs.append(f"[SKIP-DUPLICATE] {step}")
                continue

            tool_fn = TOOL_REGISTRY.get(step)
            if tool_fn is None:
                logs.append(f"[UNKNOWN] {step}")
                continue

            try:
                state = tool_fn(state)
                executed.add(step)
                logs.append(f"[OK] {step}")

            except Exception as e:
                error_msg = str(e)
                logs.append(f"[ERROR] {step}: {error_msg}")

                # Surface LLM errors directly to user via response fields
                if step in self.LLM_TOOLS:
                    # Map each LLM tool to the state key it would have set
                    key_map = {
                        "analyze_sentiment": "sentiment",
                        "explain_code":      "code_explanation",
                        "summarize":         "summary",
                        "compare_inputs":    "cross_input",
                        "chat_response":     "response",
                    }
                    target_key = key_map.get(step, "response")
                    state[target_key] = f"❌ {error_msg}"
                    # Still mark as executed so we don't retry
                    executed.add(step)

        return state, logs
