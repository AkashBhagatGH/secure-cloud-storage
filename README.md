# Secure Cloud Storage

A secure file storage system built with Python and Flask that encrypts files on upload and decrypts them for download using AES-based encryption.

## Features
✅ Upload files securely  
✅ Encrypt files with AES-Fernet  
✅ Store only encrypted files  
✅ Decrypt on demand for download  
✅ Clean Flask backend architecture

## Tech Stack
- Python  
- Flask  
- Cryptography (Fernet AES)

## Setup

1. Clone this repo  
2. Create and activate a Python virtualenv  
3. Install dependencies: `pip install -r requirements.txt`  
4. Run: `python app.py`

---

## Security Notes
- Encryption key (`secret.key`) is **not** committed to GitHub  
- Uploaded and encrypted files are ignored via `.gitignore`
