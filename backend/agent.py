# from os import path

from backend.agents.router import Router
from backend.agents.planner import Planner
from backend.agents.executor import Executor


class Agent:

    def __init__(self):
        self.router = Router()
        self.planner = Planner()
        self.executor = Executor()

    def run(self, query: str, file_path: str):

        routing = self.router.detect_intent(query)
    
        if routing["needs_clarification"]:
            return routing

        intent = routing["intent"]

        file_types = []

        

        if file_path.lower().endswith(".pdf"):
            file_types.append("pdf")

        if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            file_types.append("image")

        if file_path.lower().endswith((".mp3",".mp4", ".wav", ".m4a")):
            file_types.append("audio")

        plan = self.planner.create_plan(
            intent=intent,
            file_types=file_types
        )


        state = {
            "file_path": file_path,
            "query": query,
                "contents": {
                    "pdf": [],
                    "image": [],
                    "audio": [],
                    "youtube": [],
                 }
        }

        final_state, logs = self.executor.execute(plan, state)

        return {
            "intent": intent,
            "plan": plan,
            "logs": logs,
            "final_state": final_state
        }

if __name__ == "__main__":

    agent = Agent()

    # response = agent.run(
    #     query="Summarize this PDF",
    #     file_types=["pdf"]
    # )

    print("\nFinal Response:")
    # print(response)
    response = agent.run(
    query="Summarize this PDF",
    file_path="sample_data/project_ytlink.pdf"
    )

    # response = agent.run(
    # query="Summarize this image",
    # file_path="sample_data/sample1.jpeg"
    # )
    # response = agent.run(
    # query="Summarize this audio",
    # file_path="sample_data/sample_audio.mp4"
    # )

    # response = agent.run(
    # query="Summarize all content",
    # file_paths=[
    #     "sample_data/project_ytlink.pdf",
    #     "sample_data/sample1.jpeg",
    #     "sample_data/sample_audio.mp4"
    # ]
    # )

    print(response)