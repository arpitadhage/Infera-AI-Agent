from backend.tools.pdf_tool import parse_pdf
from backend.tools.summary_tool import summarize
from backend.tools.image_tool import extract_text_from_image
from backend.tools.audio_tool import transcribe_audio
from backend.tools.detect_urls import detect_urls   
from backend.tools.process_urls import process_urls
from backend.tools.youtube_tool import get_youtube_transcript
from backend.tools.docx_tool import extract_text_from_docx
from backend.tools.sentiment_tool import analyze_sentiment
from backend.tools.code_tool import explain_code, extract_code
from backend.tools.text_tool import extract_text
from backend.tools.context_builder import build_unified_context
from backend.tools.cross_input_tool import cross_input_reason
from backend.tools.conversational_tool import conversational_answer
from backend.tools.cross_input_tool import cross_input_reason
from backend.tools.tools import (
    extract_pdf_text,
    extract_image_text,
    transcribe_audio,
    extract_code,
    extract_text,
    summarize,
    analyze_sentiment,
    explain_code,
    chat_response,
    build_unified_context,
    compare_inputs
)

TOOLS = {
    "parse_pdf": extract_pdf_text,
    "extract_image_text": extract_image_text,
    "transcribe_audio": transcribe_audio,
    "extract_code": extract_code,
    "extract_text": extract_text,

    "summarize": summarize,
    "analyze_sentiment": analyze_sentiment,
    "explain_code": explain_code,
    "conversation": chat_response,
    "build_unified_context": build_unified_context,
    "compare_inputs": compare_inputs,
}