class Router:

    def detect_intent(self, query: str):

        query = query.lower()

        if any(word in query for word in ["summarize", "summary", "summarise"]):
            return {
                "intent": "summarization",
                "needs_clarification": False
            }

        elif any(word in query for word in ["sentiment", "emotion", "feeling"]):
            return {
                "intent": "sentiment_analysis",
                "needs_clarification": False
            }

        elif any(word in query for word in ["explain", "code", "bug", "complexity"]):
            return {
                "intent": "code_explanation",
                "needs_clarification": False
            }

        elif any(word in query for word in ["compare", "same topic", "difference"]):
            return {
                "intent": "comparison",
                "needs_clarification": False
            }
        if query.lower() in ["hi", "hello", "hey", "what can you do", "help"]:
            return {
                "intent": "conversation",
                "needs_clarification": False
    }

        return {
            "intent": None,
            "needs_clarification": True,
            "question": (
                "Could you clarify what you want me to do? "
                "For example: summarize, sentiment analysis, explain code, or compare."
            )
        }
    
if __name__ == "__main__":

    router = Router()

    result = router.detect_intent(
        "Analyze this PDF"
    )

    print(result)