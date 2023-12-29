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
    # Image processing code as previously provided

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
