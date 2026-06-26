import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class Router:
    """
    Detects the user's intent using Groq LLM.
    Returns a structured routing dict with intent and clarification flag.
    """

    VALID_INTENTS = [
        "summarization",
        "sentiment_analysis",
        "code_explanation",
        "conversation",
        "cross_input_reasoning",
        "comparison",
    ]

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def detect_intent(self, query: str, file_types: list[str] | None = None) -> dict:
        file_types = file_types or []

        # If multiple diverse files → always cross_input_reasoning / comparison
        if len(file_types) > 1:
            has_comparison_word = any(
                w in query.lower()
                for w in ["compare", "same", "different", "similar", "match", "vs", "versus", "contrast"]
            )
            intent = "comparison" if has_comparison_word else "cross_input_reasoning"
            return {"intent": intent, "needs_clarification": False}

        system_prompt = """You are an intent classifier for a multi-modal AI agent.
Classify the user query into exactly ONE of these intents:
- summarization       → user wants a summary of content
- sentiment_analysis  → user wants sentiment/emotion analysis
- code_explanation    → user wants code explained or reviewed
- comparison          → user wants to compare two or more inputs
- cross_input_reasoning → user wants insights across multiple inputs
- conversation        → general chat, greetings, questions with no file

Rules:
- Reply with ONLY the intent label, nothing else.
- If unclear but files exist, pick summarization.
- If no files and no clear task, pick conversation.
"""

        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}\nFile types: {file_types}"},
                ],
                max_tokens=20,
                temperature=0,
            )
            raw = response.choices[0].message.content.strip().lower()
            intent = raw if raw in self.VALID_INTENTS else "summarization"
        except Exception:
            intent = "summarization" if file_types else "conversation"

        return {"intent": intent, "needs_clarification": False}
