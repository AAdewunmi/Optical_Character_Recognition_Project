from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from ocr_utils import extract_text_from_image

# Initialize the Flask application
app = Flask(__name__)

# Configure the upload folder where uploaded images will be saved
app.config['UPLOAD_FOLDER'] = 'uploads'
# Set a maximum content length for uploaded files (10MB in this case)
# to prevent large uploads
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Define a default image filename to display when no image is uploaded yet
DEFAULT_IMAGE = 'Optical_blank.png'


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page of the OCR application.

    On GET request, it renders the initial page with a default blank image.
    On POST request, it processes the uploaded image, extracts text using OCR,
    and renders the page with the uploaded image and the extracted text.

    Returns:
        render_template: Renders the 'index.html' template with the
        extracted text and image filename.
    """
    extracted_text = None
    image_filename = DEFAULT_IMAGE

    if request.method == 'POST':
        # Check if an image file was included in the POST request
        if 'image' in request.files:
            image_file = request.files['image']
            # Check if the file exists and has a filename
            if image_file and image_file.filename:
                image_filename = image_file.filename
                # Construct the full path to save the uploaded image
                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], image_filename
                )
                # Save the uploaded image to the specified folder
                image_file.save(image_path)
                # Call the OCR utility function to extract text from the saved
                # image
                extracted_text = extract_text_from_image(image_path)

    # Render the 'index.html' template, passing the extracted text and
    # image filename
    return render_template(
        'index.html',
        extracted_text=extracted_text,
        image_filename=image_filename
    )


@app.route('/reset', methods=['POST'])
def reset():
    """
    Handles the reset functionality.

    On POST request to this route, it redirects the user back to the main
    index page, effectively resetting the displayed image and extracted text.

    Returns:
        redirect: Redirects the user to the 'index' route.
    """
    # Just redirect to index() which will load with default values
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serves the uploaded image files.

    This route is used to display the uploaded image in the web page.
    It retrieves the requested file from the configured upload folder.

    Args:
        filename (str): The name of the file to retrieve.

    Returns:
        send_from_directory: Sends the requested file from the upload folder.

    Example:
        If an uploaded image is named 'test.png', this route would be accessed
        via '/uploads/test.png'.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Ensure the upload folder exists when the application starts
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Run the Flask development server
    app.run(debug=True)
