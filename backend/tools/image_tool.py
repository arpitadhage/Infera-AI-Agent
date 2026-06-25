import cv2
import pytesseract
from PIL import Image
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text_from_image(state):

    files = state.get("files", [])

    image_texts = []

    for file_path in files:

        if file_path.lower().endswith((".png", ".jpg", ".jpeg")):

            img = Image.open(file_path)

            text = pytesseract.image_to_string(img)

            image_texts.append({
                "text": text,
                "source": file_path
            })

    state["contents"]["image"] = image_texts

    return state