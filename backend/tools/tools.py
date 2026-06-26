"""
tools.py — All extraction + analysis tools for DataSmith AI Agent.
Every tool receives `state` dict and returns updated `state`.
Groq is used ONLY for analysis (summarize, sentiment, code explain, compare, chat).
Extraction tools (PDF, OCR, audio) are fully local — no Groq needed.
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()

_groq_client = None

def _get_client():
    global _groq_client
    if _groq_client is None:
        from groq import Groq
        _groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _groq_client


def _llm(system: str, user: str, max_tokens: int = 1500) -> str:
    """
    Call Groq LLM. Returns a clean string.
    Raises a descriptive RuntimeError on any failure so executor can surface it.
    """
    key = os.getenv("GROQ_API_KEY", "")
    if not key or key == "your_groq_api_key_here":
        raise RuntimeError(
            " GROQ_API_KEY is not set.\n\n"
            "1. Open your .env file\n"
            "2. Set: GROQ_API_KEY=gsk_xxxxxxxxxxxx\n"
            "3. Restart the backend"
        )

    client = _get_client()
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()



def _files_of_type(state: dict, *extensions: str) -> list:
    result = []
    for path in state.get("files", []):
        if isinstance(path, str) and path.lower().endswith(extensions):
            result.append(path)
    return result


def _append_text(state: dict, items: list):
    """Append extracted text items to the shared text pool."""
    if items:
        existing = state["contents"].get("text") or []
        state["contents"]["text"] = existing + items



# EXTRACTION TOOLS


def extract_pdf_text(state: dict) -> dict:
    import fitz  # PyMuPDF
    pdfs = _files_of_type(state, ".pdf")
    extracted = []
    for path in pdfs:
        try:
            doc = fitz.open(path)
            pages_text = []
            for page in doc:
                t = page.get_text().strip()
                if t:
                    pages_text.append(t)
            doc.close()
            label = f"[PDF: {os.path.basename(path)}]"
            if pages_text:
                extracted.append(f"{label}\n" + "\n".join(pages_text))
            else:
                extracted.append(f"{label} ⚠️ No text layer found (scanned PDF?).")
        except Exception as e:
            extracted.append(f"[PDF ERROR: {os.path.basename(path)}] {e}")

    state["contents"]["pdf"] = extracted
    _append_text(state, extracted)
    return state


def extract_image_text(state: dict) -> dict:
    images = _files_of_type(state, ".png", ".jpg", ".jpeg", ".webp", ".bmp")
    extracted = []
    for path in images:
        label = f"[Image: {os.path.basename(path)}]"
        try:
            from PIL import Image
            import pytesseract
            img = Image.open(path)
            text = pytesseract.image_to_string(img).strip()
            if text:
                extracted.append(f"{label}\n{text}")
            else:
                extracted.append(f"{label} ⚠️ OCR returned no text (image may not contain readable text).")
        except ImportError:
            extracted.append(f"{label} ⚠️ OCR unavailable — install: pip install pillow pytesseract")
        except Exception as e:
            extracted.append(f"[Image ERROR: {os.path.basename(path)}] {e}")

    state["contents"]["image"] = extracted
    _append_text(state, extracted)
    return state


def transcribe_audio(state: dict) -> dict:
    audio_files = _files_of_type(state, ".mp3", ".mp4", ".wav", ".m4a", ".ogg")
    extracted = []
    for path in audio_files:
        label = f"[Audio: {os.path.basename(path)}]"
        try:
            client = _get_client()
            with open(path, "rb") as f:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=f,
                    response_format="text",
                )
            text = str(transcription).strip()
            extracted.append(f"{label}\n{text}" if text else f"{label} ⚠️ No speech detected.")
        except Exception as e:
            extracted.append(f"[Audio ERROR: {os.path.basename(path)}] {e}")

    state["contents"]["audio"] = extracted
    _append_text(state, extracted)
    return state


def extract_docx_text(state: dict) -> dict:
    docs = _files_of_type(state, ".docx")
    extracted = []
    for path in docs:
        label = f"[DOCX: {os.path.basename(path)}]"
        try:
            from docx import Document
            doc = Document(path)
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            extracted.append(f"{label}\n{text.strip()}" if text else f"{label} ⚠️ Empty document.")
        except ImportError:
            extracted.append(f"{label} ⚠️ Install python-docx: pip install python-docx")
        except Exception as e:
            extracted.append(f"[DOCX ERROR: {os.path.basename(path)}] {e}")

    state["contents"]["docx"] = extracted
    _append_text(state, extracted)
    return state


def extract_code(state: dict) -> dict:
    CODE_EXTS = (".py", ".java", ".cpp", ".js", ".c", ".cs", ".rb", ".go",
                 ".php", ".ts", ".html", ".css", ".rs")
    code_files = _files_of_type(state, *CODE_EXTS)
    extracted = []
    for path in code_files:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read().strip()
            ext = os.path.splitext(path)[1].lstrip(".")
            label = f"[Code ({ext}): {os.path.basename(path)}]"
            extracted.append(f"{label}\n```{ext}\n{content}\n```")
        except Exception as e:
            extracted.append(f"[Code ERROR: {os.path.basename(path)}] {e}")

    state["contents"]["code"] = extracted
    _append_text(state, extracted)
    return state


def extract_text(state: dict) -> dict:
    txt_files = _files_of_type(state, ".txt", ".md", ".csv", ".log")
    extracted = []
    for path in txt_files:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read().strip()
            label = f"[Text: {os.path.basename(path)}]"
            extracted.append(f"{label}\n{content}" if content else f"{label} ⚠️ Empty file.")
        except Exception as e:
            extracted.append(f"[Text ERROR: {os.path.basename(path)}] {e}")

    existing = state["contents"].get("text") or []
    state["contents"]["text"] = existing + extracted
    return state


def fetch_youtube_transcript(state: dict) -> dict:
    query = state.get("query", "")
    yt_pattern = re.compile(r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+")
    match = yt_pattern.search(query)
    if not match:
        state["contents"]["youtube"] = ["[YouTube] ⚠️ No YouTube URL found in query."]
        return state

    url = match.group(0)
    if not url.startswith("http"):
        url = "https://" + url

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        vid_id = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url).group(1)
        transcript = YouTubeTranscriptApi.get_transcript(vid_id)
        text = " ".join(t["text"] for t in transcript)
        label = f"[YouTube: {url}]"
        yt_result = [f"{label}\n{text.strip()}"]
        state["contents"]["youtube"] = yt_result
        _append_text(state, yt_result)
    except ImportError:
        state["contents"]["youtube"] = ["[YouTube] ⚠️ Install: pip install youtube-transcript-api"]
    except Exception as e:
        state["contents"]["youtube"] = [f"[YouTube ERROR: {url}] {e}"]

    return state

# ANALYSIS TOOLS

def analyze_sentiment(state: dict) -> dict:
    texts = state.get("contents", {}).get("text") or []
    if not texts:
        state["sentiment"] = "⚠️ No text was extracted. Please upload a readable file."
        return state

    combined = "\n\n".join(texts)[:4000]
    state["sentiment"] = _llm(
        system=(
            "You are a professional sentiment analysis engine. "
            "Analyze sentiment of the provided text. Return:\n"
            "• Overall Sentiment: Positive / Negative / Neutral / Mixed\n"
            "• Confidence: High / Medium / Low\n"
            "• Key Emotional Tones: (list 3-5)\n"
            "• Summary: 2-sentence overview\n"
            "• Evidence: Quote 2-3 phrases that support your verdict."
        ),
        user=f"Analyze the sentiment:\n\n{combined}",
        max_tokens=600,
    )
    return state


def explain_code(state: dict) -> dict:
    codes = state.get("contents", {}).get("code") or []
    if not codes:
        codes = state.get("contents", {}).get("text") or []
    if not codes:
        state["code_explanation"] = "⚠️ No code found to explain."
        return state

    combined = "\n\n".join(codes)[:4000]
    state["code_explanation"] = _llm(
        system=(
            "You are a senior software engineer and code reviewer. "
            "Explain the code clearly covering:\n"
            "1. What it does (overview)\n"
            "2. How it works (key logic)\n"
            "3. Key functions / classes\n"
            "4. Potential bugs or issues\n"
            "5. Improvement suggestions"
        ),
        user=f"Explain this code:\n\n{combined}",
        max_tokens=1000,
    )
    return state


def summarize(state: dict) -> dict:
    texts = state.get("contents", {}).get("text") or []
    if not texts:
        state["summary"] = "⚠️ No content was extracted. Check the file format is supported."
        return state

    combined = "\n\n".join(texts)[:4500]
    state["summary"] = _llm(
        system=(
            "You are a professional summarizer. "
            "Produce a clear, well-structured summary with:\n"
            "• Main Topic\n"
            "• Key Points (bullet list)\n"
            "• Important Details\n"
            "• Conclusion / Takeaway"
        ),
        user=f"Summarize the following content:\n\n{combined}",
        max_tokens=900,
    )
    return state


def build_unified_context(state: dict) -> dict:
    contents = state.get("contents", {})
    parts = []
    for key, items in contents.items():
        if isinstance(items, list):
            parts.extend(i for i in items if i)
        elif isinstance(items, str) and items:
            parts.append(items)
    state["unified_context"] = "\n\n".join(parts)
    return state


def compare_inputs(state: dict) -> dict:
    contents = state.get("contents", {})
    sections = []
    for key, items in contents.items():
        if isinstance(items, list):
            for item in items:
                if item and not item.endswith("[]"):
                    sections.append(item)

    if len(sections) < 2:
        state["cross_input"] = (
            "⚠️ Need at least 2 inputs to compare.\n"
            "Upload 2+ files (e.g. a PDF and an audio file) and ask:\n"
            "  'Compare these' or 'Are these the same?'"
        )
        return state

    combined = "\n\n---SEPARATOR---\n\n".join(sections)[:5000]
    state["cross_input"] = _llm(
        system=(
            "You are a cross-document comparison expert. "
            "Given multiple labelled inputs, compare them thoroughly:\n\n"
            "1. **Same or Different?** Do they cover the same topic/data?\n"
            "2. **Overlapping Content** — what's shared between them?\n"
            "3. **Unique to each** — what's only in one input?\n"
            "4. **Similarity Score** — 0-100% with justification\n"
            "5. **Verdict** — Consistent / Partially consistent / Contradictory\n\n"
            "Be specific and cite which document each point comes from."
        ),
        user=f"Compare these inputs:\n\n{combined}",
        max_tokens=1200,
    )
    return state


def chat_response(state: dict) -> dict:
    query = state.get("query", "Hello!")
    state["response"] = _llm(
        system=(
            "You are DataSmith AI Agent — a helpful, knowledgeable assistant "
            "specializing in document analysis, code review, sentiment analysis, "
            "and multi-modal reasoning. Be friendly and concise. "
            "If greeted, introduce yourself and list your capabilities briefly."
            "You are DataSmith AI Agent. Always answer in clean, beautiful Markdown. Use a clear heading, a short introduction, bold section titles, bullet points for key information, and readable paragraphs. If summarizing, include: 1) One-line Summary, 2) Three Key Points, 3) Detailed Explanation, and if multiple inputs are provided, include a Cross-Input Relationship section with Connected, Partially Connected, or Not Related along with reasoning. If performing sentiment analysis, return Sentiment, Confidence, and Justification. If explaining code, return Overview, Working, Bugs (if any), and Time Complexity. For conversations, respond naturally and helpfully. Never output JSON, Python dictionaries, HTML, XML, escaped characters, or raw data structures. Always produce clean, user-friendly, well-formatted Markdown."
        ),
        user=query,
        max_tokens=600,
    )
    return state
