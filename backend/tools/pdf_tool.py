import fitz

import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text
def parse_pdf(state):

    files = state.get("files", [])

    pdf_texts = []

    for file_path in files:

        if file_path.lower().endswith(".pdf"):

            text = extract_text_from_pdf(file_path)

            pdf_texts.append({
                "text": text,
                "source": file_path
            })

    state["contents"]["pdf"] = pdf_texts

    return state