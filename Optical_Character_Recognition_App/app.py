from flask import Flask, render_template, request
import os
from ocr_utils import extract_text_from_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file and image_file.filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)
            extracted_text = extract_text_from_image(image_path)
    return render_template('index.html', extracted_text=extracted_text)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
