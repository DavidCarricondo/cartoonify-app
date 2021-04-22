from flask import Flask, render_template, request, redirect, flash, url_for
import requests
from src.utils import CARTOON

app = Flask('__name__')

@app.route('/')
def welcome():
    return render_template('index.html')


##TODO:
@app.route('/<image_path>', methods=['POST'])
def cartoon():
    output_image = CARTOON().fit_transform('models/Hosoda_net_G_float.pth', image_path)
    return 'Did it, good job'

if __name__ == '__main__':
    app.run('0.0.0.0',5000, debug=True)