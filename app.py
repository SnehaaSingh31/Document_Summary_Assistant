from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from extractors import extract_text_from_pdf, extract_text_from_image, OCR_AVAILABLE
from summarizer import summarize_text, improvement_suggestions

ALLOWED_EXTS = {'.pdf', '.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ocr_available=OCR_AVAILABLE)

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': 'No file part in request'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'ok': False, 'error': 'No file selected'}), 400

    length = request.form.get('length', 'medium').lower()
    if length not in {'short','medium','long'}:
        length = 'medium'

    filename = secure_filename(f.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(save_path)

    _, ext = os.path.splitext(filename.lower())

    try:
        if ext == '.pdf':
            text = extract_text_from_pdf(save_path)
        elif ext in {'.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff'}:
            text = extract_text_from_image(save_path)
        else:
            return jsonify({'ok': False, 'error': 'Unsupported file type'}), 400

        if not text or not text.strip():
            return jsonify({'ok': False, 'error': 'No extractable text found. If this is a scanned PDF, OCR for PDFs is not enabled in this minimal build.'}), 422

        summary, key_points = summarize_text(text, length=length)
        tips = improvement_suggestions(text)

        return jsonify({
            'ok': True,
            'extracted_chars': len(text),
            'summary': summary,
            'key_points': key_points,
            'suggestions': tips,
            'ocr_available': OCR_AVAILABLE
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
