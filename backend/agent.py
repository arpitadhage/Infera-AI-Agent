# from os import path

from importlib.resources import files

from backend.agents.router import Router
from backend.agents.planner import Planner
from backend.agents.executor import Executor
from dotenv import load_dotenv
load_dotenv()

class Agent:

    def __init__(self):
        self.router = Router()
        self.planner = Planner()
        self.executor = Executor()

    def run(self, query: str, file_path):

        routing = self.router.detect_intent(query)
    
        if routing["needs_clarification"]:
            return routing

        intent = routing["intent"]

        file_types = []

        files = file_path if isinstance(file_path, list) else [file_path]

        for path in files:

            if path.lower().endswith(".pdf"):
                file_types.append("pdf")

            if path.lower().endswith((".png", ".jpg", ".jpeg")):
                file_types.append("image")

            if path.lower().endswith((".mp3",".mp4", ".wav", ".m4a")):
                file_types.append("audio")
        
            if path.lower().endswith(".docx"):
                file_types.append("docx")

            if path.endswith((".py", ".java", ".cpp", ".js", ".c", ".cs", ".rb", ".go", ".php", ".ts")):
                file_types.append("code")

        plan = self.planner.create_plan(
            intent=intent,
            file_types=file_types
        )


        state = {
            "files": files,
            "query": query,
                "contents": {
                    "pdf": [],
                    "image": [],
                    "audio": [],
                    "youtube": [],
                    "docx": [],
                    "code": [],
                    "text": []
                 },
                 "unified_context": "" 
        }

        final_state, logs = self.executor.execute(plan, state)

        return {
            "intent": intent,
            "plan": plan,
            "logs": logs,
            "final_state": final_state
        }

# if __name__ == "__main__":

#     agent = Agent()

    # response = agent.run(
    #     query="Summarize this PDF",
    #     file_types=["pdf"]
    # )

    # print("\nFinal Response:")
    # print(response)
    # response = agent.run(
    # query="Summarize this PDF",
    # file_path="sample_data/project_ytlink.pdf"
    # )

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
#     response = agent.run(
#     query="Analyze sentiment",
#     file_path="sample_data/review2.txt"
# )
# response = agent.run(
#         query="hello",
#         file_path=""
#     )
# print(response)

# response = agent.run(
#     query="Explain this code",
#     file_path="sample_data/test.py"
# )

# print(response["final_state"]["code_explanation"])
   

# response = agent.run(
#     query="Summarize this PDF + image + audio",
#     file_path=[
#         "sample_data/sample.pdf",
#         "sample_data/sample1.jpeg",
#         "sample_data/sample_audio.mp4"
#     ]
# )

# print(response["final_state"]["summary"])