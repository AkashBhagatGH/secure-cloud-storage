from flask import Flask, render_template, request, send_file
import os
import io
import boto3
from encryption import encrypt_file, decrypt_file

# -------------------------------
# AWS S3 CONFIGURATION
# -------------------------------
s3 = boto3.client("s3")
BUCKET_NAME = "secure-cloud-storage-akash"

# -------------------------------
# FLASK APP SETUP
# -------------------------------
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)


# -------------------------------
# HELPER: LIST FILES FROM S3
# -------------------------------
def get_files_from_s3():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        return [
            obj["Key"].replace(".enc", "")
            for obj in response.get("Contents", [])
            if obj["Key"].endswith(".enc")
        ]
    except Exception:
        return []


# -------------------------------
# HOME + UPLOAD ROUTE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    files = get_files_from_s3()

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return render_template(
                "index.html",
                files=files,
                message="No file selected",
                message_type="error"
            )

        original_path = os.path.join(UPLOAD_FOLDER, file.filename)
        encrypted_path = os.path.join(
            ENCRYPTED_FOLDER, file.filename + ".enc"
        )

        try:
            # Save plaintext temporarily
            file.save(original_path)

            # Encrypt locally
            encrypt_file(original_path, encrypted_path)

            # Upload encrypted file to S3
            s3.upload_file(
                encrypted_path,
                BUCKET_NAME,
                file.filename + ".enc"
            )

        except Exception:
            return render_template(
                "index.html",
                files=files,
                message="Upload failed. Please try again.",
                message_type="error"
            )

        finally:
            # Always clean up local files
            if os.path.exists(original_path):
                os.remove(original_path)
            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)

        files = get_files_from_s3()
        return render_template(
            "index.html",
            files=files,
            message="File uploaded and encrypted successfully",
            message_type="success"
        )

    return render_template("index.html", files=files)


# -------------------------------
# DOWNLOAD ROUTE
# -------------------------------
@app.route("/download/<filename>")
def download(filename):
    encrypted_path = os.path.join(
        ENCRYPTED_FOLDER, filename + ".enc"
    )
    decrypted_path = os.path.join(
        UPLOAD_FOLDER, "decrypted_" + filename
    )

    try:
        # Download encrypted file from S3
        s3.download_file(
            BUCKET_NAME,
            filename + ".enc",
            encrypted_path
        )

        # Decrypt locally
        decrypt_file(encrypted_path, decrypted_path)

        # Read decrypted file into memory
        with open(decrypted_path, "rb") as f:
            file_bytes = f.read()

    except Exception:
        files = get_files_from_s3()
        return render_template(
            "index.html",
            files=files,
            message="Download failed or file not found",
            message_type="error"
        )

    finally:
        # Cleanup temp files
        if os.path.exists(encrypted_path):
            os.remove(encrypted_path)
        if os.path.exists(decrypted_path):
            os.remove(decrypted_path)

    # Send file safely from memory
    return send_file(
        io.BytesIO(file_bytes),
        as_attachment=True,
        download_name=filename
    )


# -------------------------------
# DELETE ROUTE
# -------------------------------
@app.route("/delete/<filename>")
def delete_file(filename):
    try:
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=filename + ".enc"
        )

        message = "File deleted successfully"
        message_type = "success"

    except Exception:
        message = "Failed to delete file"
        message_type = "error"

    files = get_files_from_s3()
    return render_template(
        "index.html",
        files=files,
        message=message,
        message_type=message_type
    )


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
