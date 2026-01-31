# 🔐 Secure Cloud Storage System

A secure cloud-based file storage system built using **Flask** and **AWS S3**, where files are **encrypted locally before being uploaded to the cloud**.

This project focuses on **security-first design**, clean backend architecture, and real-world cloud practices.

---

## 🚀 Features

- 🔒 Local file encryption using symmetric encryption
- ☁️ Encrypted file storage in AWS S3
- ⬆️ Upload files securely
- ⬇️ Download and decrypt files on demand
- 🗑️ Delete encrypted files from cloud storage
- 🧹 Automatic cleanup of temporary files
- 💬 Clear user feedback (success / error messages)
- 💸 Cost-safe design using empty buckets and lifecycle rules

---

## 🧠 System Architecture

### Upload Flow

```
User
 │
 ▼  Upload
Flask Server
 │  (encrypt locally)
 ▼
Encrypted File (.enc)
 │
 ▼
AWS S3 Bucket
```

### Download Flow

```
AWS S3 → Download encrypted file → Decrypt locally → Send to user → Cleanup temp files
```

---

## 🔐 Security Design

- Files are **encrypted locally** before leaving the server
- Encryption keys never leave the application environment
- AWS S3 stores **only encrypted files**
- No plaintext files are persisted
- AWS credentials are managed using **environment variables**
- No secrets are committed to GitHub

---

## ☁️ AWS Usage

- **Amazon S3** for encrypted file storage
- **IAM** with least-privilege access policy
- **Lifecycle rules** to auto-delete old files (optional)
- Zero-cost when bucket is empty

---

## 🛠️ Tech Stack

| Category     | Technology                  |
|--------------|-----------------------------|
| Backend      | Python, Flask               |
| Cloud        | AWS S3, IAM                 |
| Security     | Cryptography (Fernet)       |
| Frontend     | HTML, CSS (server-rendered) |
| File Handling| In-memory downloads (Windows-safe) |

---

## 📦 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/AkashBhagatGH/secure-cloud-storage.git
cd secure-cloud-storage
```

### 2️⃣ Create virtual environment

```bash
python -m venv env
env\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set AWS credentials (Environment Variables)

```bash
setx AWS_ACCESS_KEY_ID "YOUR_ACCESS_KEY"
setx AWS_SECRET_ACCESS_KEY "YOUR_SECRET_KEY"
setx AWS_DEFAULT_REGION "ap-south-1"
```

### 5️⃣ Run the application

```bash
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)
