import os

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

app = Flask(__name__, template_folder='template')

app.config['ALLOWED_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_FOLDER'] = 'uploads'

def generate_key():
    key = Fernet.generate_key()
    with open('klucz.key', 'wb') as key_file:
        key_file.write(key)


def load_key():
    return open('klucz.key', 'rb').read()


def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message)
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message



def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in app.config['ALLOWED_EXTENSIONS'])



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        generate_key()
        key = load_key()

        with open(file_path, 'rb') as plaintext_file:
            plaintext = plaintext_file.read()

        encrypted_message = encrypt_message(plaintext, key)
        with open('mySecret.txt', 'wb') as file:
            file.write(encrypted_message)

        return "plik zaszyfrowany - mySecret.txt"

    return "Invalid file format"

@app.route('/d')
def decrypt():
    return render_template('decrypt.html')

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        key = load_key()

        with open(file_path, 'rb') as encrypted_file:
            encrypted_message = encrypted_file.read()

        decrypted_message = decrypt_message(encrypted_message, key)

        
        decrypted_file_path = os.path.splitext(file_path)[0] + '_decrypted.txt'
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_message)

        return "plik odszyfrowany - mySecret_decrypted.txt"


    return "Invalid file format"





if __name__ == '__main__':
    app.run(debug=True)