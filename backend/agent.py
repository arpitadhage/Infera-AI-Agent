import os
from backend.agents.router import Router
from backend.agents.planner import Planner
from backend.agents.executor import Executor
from dotenv import load_dotenv

load_dotenv()

EXT_TYPE_MAP = {
    ".pdf":  "pdf",
    ".png":  "image", ".jpg": "image", ".jpeg": "image", ".webp": "image", ".bmp": "image",
    ".mp3":  "audio", ".mp4": "audio", ".wav":  "audio", ".m4a": "audio", ".ogg": "audio",
    ".docx": "docx",
    ".py":   "code",  ".java": "code", ".cpp":  "code", ".js":  "code",
    ".c":    "code",  ".cs":   "code", ".rb":   "code", ".go":  "code",
    ".php":  "code",  ".ts":   "code", ".html": "code", ".rs":  "code",
    ".txt":  "txt",   ".md":   "txt",  ".csv":  "txt",  ".log": "txt",
}


def _classify_files(file_paths: list) -> list:
    types, seen = [], set()
    for path in file_paths:
        if not isinstance(path, str) or not path:
            continue
        ext = os.path.splitext(path)[1].lower()
        ftype = EXT_TYPE_MAP.get(ext)
        if ftype and ftype not in seen:
            seen.add(ftype)
            types.append(ftype)
    return types


class Agent:
    def __init__(self):
        self.router   = Router()
        self.planner  = Planner()
        self.executor = Executor()

    def run(self, query: str, file_path) -> dict:
        # 1. Normalize paths
        if isinstance(file_path, list):
            files = [p for p in file_path if isinstance(p, str) and p]
        elif isinstance(file_path, str) and file_path:
            files = [file_path]
        else:
            files = []

        # 2. Classify
        file_types = _classify_files(files)

        # 3. Route
        routing = self.router.detect_intent(query, file_types=file_types)
        if routing.get("needs_clarification"):
            return {"response": routing.get("message", "Please clarify."), "plan": []}

        intent = routing["intent"]

        # 4. Plan
        plan = self.planner.create_plan(intent=intent, file_types=file_types)

        # 5. State
        state = {
            "files": files,
            "query": query,
            "contents": {
                "pdf": [], "image": [], "audio": [],
                "docx": [], "code": [], "text": [], "youtube": [],
            },
            "unified_context": "",
        }

        # 6. Execute
        final_state, logs = self.executor.execute(plan, state)

        # 7. Response 
        response = next(
            (v for v in [
                final_state.get("cross_input"),
                final_state.get("summary"),
                final_state.get("sentiment"),
                final_state.get("code_explanation"),
                final_state.get("response"),
            ] if v),
            "⚠️ No response generated. Check your GROQ_API_KEY in .env"
        )

       
        raw = final_state.get("contents", {})
        extracted_text = {k: v for k, v in raw.items() if v}

        return {
            "response":      response,
            "plan":          plan,
            "logs":          logs,
            "intent":        intent,
            "extracted_text": extracted_text,
        }
