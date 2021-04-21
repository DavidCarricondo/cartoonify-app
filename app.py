from flask import Flask
import requests
from src.utils import CARTOON

app = Flask('__name__')

@app.route('/')
def welcome():
    return 'Welcome to my cartoonify (WIP)'
##TODO:
@app.route('/cartoon', methods=['POST'])
def cartoon():
    picture = requests.data
    return CARTOON().fit_transform('models/Hosoda_net_G_float.pth', picture)

if __name__ == '__main__':
    app.run('0.0.0.0',5000, debug=True)