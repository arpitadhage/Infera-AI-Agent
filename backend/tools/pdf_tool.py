import fitz

import fitz  # PyMuPDF




def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    doc.close()

    return text.strip()


def parse_pdf(state):

    files = state.get("files", [])

    pdf_texts = []

    for file_path in files:

        if file_path.lower().endswith(".pdf"):

            text = extract_text_from_pdf(file_path)

            if text.strip():
                pdf_texts.append({
                    "text": text,
                    "source": file_path
                })
            else:
                pdf_texts.append({
                    "text": "[NO EXTRACTABLE TEXT - POSSIBLY SCANNED PDF]",
                    "source": file_path
                })

    state["contents"]["pdf"] = pdf_texts

    return state