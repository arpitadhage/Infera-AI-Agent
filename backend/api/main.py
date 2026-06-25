from fastapi import FastAPI, UploadFile, File, Form
from backend.agent import Agent
import shutil
import os

app = FastAPI()

agent = Agent()


@app.post("/run-agent")
async def run_agent(
    query: str = Form(...),
    file: UploadFile = File(None)
):

    file_path = ""

    # save uploaded file
    if file:
        file_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # run agent
    response = agent.run(
        query=query,
        file_path=file_path
    )

    return response

@app.get("/")
def health():
    return {"status": "Agent API running 🚀"}