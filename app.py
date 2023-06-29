import os

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

app = Flask(__name__, template_folder='template')

app.config['ALLOWED_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_FOLDER'] = 'uploads'





if __name__ == '__main__':
    app.run(debug=True)