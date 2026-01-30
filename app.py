from flask import Flask, render_template, request, send_file
import os
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        encrypted_path = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")

        file.save(upload_path)
        encrypt_file(upload_path, encrypted_path)

        return "File uploaded and encrypted successfully!"

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, filename + ".enc")
    if not os.path.exists(encrypted_path):
        return "File not Found"
    decrypted_path = os.path.join(UPLOAD_FOLDER, "decrypted_" + filename)

#Take the encrypted file and convert it back into the original file.
    decrypt_file(encrypted_path, decrypted_path)

    return send_file(decrypted_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
