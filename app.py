from flask import Flask, request, send_file, render_template
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'output/'

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def convert_to_pencil_sketch(input_path, output_path, text):
    # Read the image
    image = cv2.imread(input_path)
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert the grayscale image
    inverted_image = 255 - gray_image
    # Blur the inverted image
    blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    # Invert the blurred image
    inverted_blurred = 255 - blurred_image
    # Create the pencil sketch image
    sketch_image = cv2.divide(gray_image, inverted_blurred, scale=256.0)

    # Convert to PIL Image to add text
    pil_img = Image.fromarray(sketch_image)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.load_default()  # You can also use a specific font here
    # Add text
    draw.text((10, 10), text, (255, 255, 255), font=font)

    # Save the final image
    pil_img.save(output_path, "JPEG")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'sketch_' + filename)
            file.save(input_path)
            convert_to_pencil_sketch(input_path, output_path, "Kishor Ravikumar")
            return send_file(output_path, as_attachment=True)
    return '''
    <!doctype html>
    <title>Upload Image</title>
    <h1>Upload Image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
