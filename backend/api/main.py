import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from backend.agent import Agent

app = FastAPI(title="DataSmith AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()
TEMP_DIR = "temp"


@app.get("/")
def health():
    return {"status": "DataSmith Agent API running 🚀"}


@app.post("/run-agent")
async def run_agent(
    query: str = Form(...),
    files: Optional[List[UploadFile]] = File(default=None),
):
    """
    Accepts:
      - query: str
      - files: 0 or more uploaded files (any supported type)

    Returns:
      - response: final agent answer
      - plan: steps executed
      - intent: detected intent
      - extracted_text: cleaned extracted content (no empty fields)
    """
    try:
        os.makedirs(TEMP_DIR, exist_ok=True)
        file_paths: list[str] = []

        # Save all uploaded files 
        if files:
            for upload in files:
                if upload and upload.filename:
                    safe_name = upload.filename.replace(" ", "_")
                    dest = os.path.join(TEMP_DIR, safe_name)
                    with open(dest, "wb") as buf:
                        shutil.copyfileobj(upload.file, buf)
                    file_paths.append(dest)

        if not query.strip() and not file_paths:
            return {
                "response": "⚠️ Please provide a query, a file, or both.",
                "plan": [],
                "error": True,
            }

        result = agent.run(query=query, file_path=file_paths)

        if not isinstance(result, dict):
            return {"response": str(result), "plan": [], "error": True}

        return result

    except Exception as e:
        return {
            "response": f"❌ Agent error: {str(e)}",
            "error": True,
            "plan": [],
        }
