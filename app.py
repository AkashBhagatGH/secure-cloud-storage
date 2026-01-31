from flask import Flask, render_template, request, send_file
import os
import io
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return render_template(
                "index.html",
                message="No file selected ❌"
            )

        # Save file temporarily
        original_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(original_path)

        # Encrypt file
        encrypted_path = os.path.join(
            ENCRYPTED_FOLDER, file.filename + ".enc"
        )
        encrypt_file(original_path, encrypted_path)

        # Remove plaintext file
        os.remove(original_path)
        files = os.listdir(ENCRYPTED_FOLDER)
        return render_template(
            "index.html",
            message="File uploaded and encrypted successfully ✅",
            download_url=f"/download/{file.filename}",
            files=files
        )
    

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    encrypted_path = os.path.join(
        ENCRYPTED_FOLDER, filename + ".enc"
    )

    if not os.path.exists(encrypted_path):
        return "File not found"

    decrypted_path = os.path.join(
        UPLOAD_FOLDER, "decrypted_" + filename
    )

    # Decrypt file
    decrypt_file(encrypted_path, decrypted_path)

    # Read decrypted file into memory
    with open(decrypted_path, "rb") as f:
        file_bytes = f.read()

    # Delete decrypted file BEFORE sending
    os.remove(decrypted_path)

    # Send file from memory (Windows-safe)
    return send_file(
        io.BytesIO(file_bytes),
        as_attachment=True,
        download_name=filename
    )

@app.route("/delete/<filename>")
def delete_file(filename):
    encrypted_path = os.path.join(
        ENCRYPTED_FOLDER, filename + ".enc"
    )
    if os.path.exists(encrypt_file):
        os.remove(encrypted_path)


if __name__ == "__main__":
    app.run(debug=True)
