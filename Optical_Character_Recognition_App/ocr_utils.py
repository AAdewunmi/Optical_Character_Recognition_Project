from PIL import Image
import pytesseract


def extract_text_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image_path (str): The file path to the image.

    Returns:
        str: The extracted text from the image. Returns an empty string if no
        text is found or if there's an error opening the image.
    """
    try:
        # Open the image using Pillow library
        image = Image.open(image_path)
        # Perform OCR using pytesseract to get the text
        text = pytesseract.image_to_string(image)
        return text
    except FileNotFoundError:
        print(f"Error: Image not found at path: {image_path}")
        return ""
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
        return ""


if __name__ == '__main__':
    # Example of how to use the extract_text_from_image function

    # 1. Make sure you have an image file (e.g., 'example.png') in the same
    #    directory or provide the full path to the image.

    # 2. Call the function with the image path
    image_file = 'example.png'  # Replace with the actual path to your image
    extracted_text = extract_text_from_image(image_file)

    # 3. Print the extracted text
    if extracted_text:
        print("Extracted Text:\n", extracted_text)
    else:
        print(
            f"Could not extract text from '{image_file}' "
            "or the image was empty."
        )

    # --- Another example with a different image path ---
    # another_image = '/path/to/another/image.jpg'
    # text_from_another = extract_text_from_image(another_image)
    # if text_from_another:
    #     print(f"\nText from '{another_image}':\n", text_from_another)
