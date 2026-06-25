class Planner:

    def create_plan(self, intent, file_types):

        plan = []

    # 1. INGESTION
        if "pdf" in file_types:
            plan.append("parse_pdf")

        if "image" in file_types:
            plan.append("extract_image_text")

        if "audio" in file_types:
            plan.append("transcribe_audio")

    # 2. URL PROCESSING (AFTER EXTRACTION)
        plan.append("detect_urls")
        plan.append("process_urls")

    # 3. CONTEXT BUILDING
        plan.append("build_unified_context")

    # 4. TASK LAYER (ONLY ONE MAIN TASK)
        if intent == "summarization":
            plan.append("summarize")

        elif intent == "sentiment_analysis":
            plan.append("analyze_sentiment")

        elif intent == "cross_input_reasoning":
            plan.append("cross_input_reason")

        elif intent == "code_explanation":
            plan.append("explain_code")
        
        if intent == "conversation":
            return["conversation"]

        if intent == "qa":
            plan.append("answer_question")

    # 5. FINAL CLEANUP
        plan = list(dict.fromkeys(plan))  # remove duplicates

        return plan
    
if __name__ == "__main__":

    planner = Planner()

    print(
        planner.create_plan(
            intent="summarization",
            file_types=["pdf"]
        )
    )