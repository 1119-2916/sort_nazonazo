import os
import io
import time
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

# from werkzeug import secure_filename

app = Flask(__name__)

# <--プログラム-->

@app.route('/')
def index():
    return 'Hello World!'

#@app.route('/post', method=['POST'])
#def post_json():

#@app.route('/show-data', methods=['POST'])
#def show_json():

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

