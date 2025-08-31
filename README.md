# Document Summary Assistant — Pro (Attractive UI + OCR-ready)

**What it does**
- Upload **PDF** or **image files** (drag-and-drop or file picker)
- Extract text:
  - PDFs → parsed via PyPDF2 (text-based PDFs)
  - Images → OCR via Tesseract (if installed)
- Generate summaries (short / medium / long) + **Key points**
- **Improvement suggestions** based on simple heuristics
- Clean, mobile-responsive UI (Bootstrap), loading states, errors
- Minimal dependencies

> Note: OCR for *scanned PDFs* is not enabled in this minimal build (requires rendering PDFs to images). Images OCR works if Tesseract is installed.

## Tech & Dependencies
- Python: Flask, PyPDF2, Pillow, pytesseract
- Frontend: Bootstrap 5 + Bootstrap Icons (CDN)

## Setup (Local)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 in your browser.

### Optional: Enable OCR for images
1) Install **Tesseract** system binary.  
2) Ensure `tesseract` is on PATH or installed at `C:\Program Files\Tesseract-OCR\tesseract.exe` (Windows).  
3) Restart the app. The header badge will show **OCR ON**.

## Deploy
- **Heroku/Render**: Provided `Procfile` and `runtime.txt`.  
- **Vercel/Netlify**: Use a Python serverless runtime or deploy via a container; easiest is Render.

## Limitations
- Scanned PDFs aren't OCR'd in this minimal build (keep dependencies small). If needed, add a renderer (e.g., `pypdfium2`) to convert pages to images before OCR.
