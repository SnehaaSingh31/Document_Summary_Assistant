import os
from PyPDF2 import PdfReader

# Try to enable OCR with pytesseract + Pillow (no hard crash if missing)
OCR_AVAILABLE = False
try:
    from PIL import Image
    import pytesseract, shutil
    # Try auto-detect tesseract, else fall back to common Windows path
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # quick sanity: if file doesn't exist, keep going; pytesseract will raise on use
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

def extract_text_from_pdf(path: str) -> str:
    """Extract text from text-based PDFs using PyPDF2."""
    text_parts = []
    reader = PdfReader(path)
    for page in reader.pages:
        content = page.extract_text() or ""
        text_parts.append(content)
    return "\n".join(text_parts)

def extract_text_from_image(path: str) -> str:
    """Extract text from image files via OCR if available."""
    if not OCR_AVAILABLE:
        raise RuntimeError("OCR not available. Install Tesseract and pytesseract to enable image text extraction.")
    from PIL import Image
    import pytesseract
    img = Image.open(path)
    # Basic pre-processing hint: convert to RGB (supports most formats), let tesseract do the rest
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    text = pytesseract.image_to_string(img, lang="eng")
    return text or ""
