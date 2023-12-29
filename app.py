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
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    
    # Convert to gray scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Invert the gray image
    inverted_img = cv2.bitwise_not(gray_img)
    
    # Blur the image by gaussian function
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), 0)
    
    # Invert the blurred image
    inverted_blur = cv2.bitwise_not(blurred_img)
    
    # Create the pencil sketch image
    sketch_img = cv2.divide(gray_img, inverted_blur, scale=256.0)
    
    # Convert to PIL Image for adding text
    pil_img = Image.fromarray(sketch_img)
    draw = ImageDraw.Draw(pil_img)
    
    # Adding text
    font_size = 30
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width, text_height = draw.textsize(text, font=font)
    x, y = pil_img.width - text_width - 10, pil_img.height - text_height - 10
    draw.text((x, y), text, (255, 255, 255), font=font)
    
    # Save the final image
    pil_img.save(output_path, "JPEG")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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

if __name__ == '__main__':
    app.run(debug=True)
