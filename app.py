from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os, re
from src.utils import CARTOON

UPLOAD_FOLDER = '/home/david/Documents/Python/cartoonify_app/static'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/cartoonify', methods=['POST'])
def cartoon():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            file.filename = 'upload_image.jpg'
            filename = secure_filename(file.filename)
            input_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(input_path)
            output_image = CARTOON().fit_transform('models/Hosoda_net_G_float.pth', input_path)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'],'output_image.jpg')
            output_image.save(output_path)
            flash('Image saved')
            return render_template('output.html')

@app.after_request
def add_header(response):
    response.cache_control.max_age=0
    return response

if __name__ == '__main__':
    app.run('0.0.0.0',5000, debug=True)

