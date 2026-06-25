from backend.tools.pdf_tool import parse_pdf
from backend.tools.summary_tool import summarize
from backend.tools.image_tool import extract_text_from_image
from backend.tools.audio_tool import transcribe_audio
# from backend.tools.comparison_tool import compare_content
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


TOOLS = {
    "parse_pdf": parse_pdf,
    "summarize": summarize,
    "extract_image_text": extract_text_from_image,
    "transcribe_audio": transcribe_audio,
    "detect_urls": detect_urls,
    "process_urls": process_urls,   
    "get_youtube_transcript": get_youtube_transcript,
    "extract_docx_text": extract_text_from_docx,
    "analyze_sentiment": analyze_sentiment,
    "extract_code": extract_code,
    "explain_code": explain_code,
    "extract_text": extract_text,
    "build_unified_context": build_unified_context,
    "cross_input_reason": cross_input_reason,
    "conversation": conversational_answer
}