from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from ocr_utils import extract_text_from_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

DEFAULT_IMAGE = 'Optical_blank.png'

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    image_filename = DEFAULT_IMAGE

    if request.method == 'POST':
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                image_filename = image_file.filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)
                extracted_text = extract_text_from_image(image_path)

    return render_template('index.html', extracted_text=extracted_text, image_filename=image_filename)

@app.route('/reset', methods=['POST'])
def reset():
    return redirect(url_for('index'))  # Just redirect to index() with default values

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

