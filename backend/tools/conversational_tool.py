def conversational_answer(state):

    query = state.get("query", "")

    response = f"""
Hello! 👋

I am your DataSmith AI Agent.

I can help you with:
- PDF / Image / Audio summarization
- Sentiment analysis
- Code explanation
- Cross-input reasoning
- YouTube transcript extraction

Just upload a file and ask your question!
"""

    state["response"] = response

    return state