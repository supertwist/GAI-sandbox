# 🧠 ComfyUI + Google Sheets + AWS S3 Pipeline  
### HPC-Ready Prompt Orchestration Engine

This project turns **Google Sheets into a live prompt queue** for **ComfyUI** running locally or on an HPC cluster (e.g., Pegasus).  

Generated images are automatically uploaded to **AWS S3**, and the Sheet updates in real time with status, output URLs, and preview thumbnails.

---

## 🚀 What This Enables

- Use Google Sheets as a no-code control panel  
- Run ComfyUI workflows remotely (Pegasus / HPC supported)  
- Automatically upload outputs to AWS S3  
- Track generation status live  
- Enable reproducible AI experiments  
- Support parallel generation  

This is infrastructure for:
- 🧪 Research experiments  
- 🔁 Prompt optimization loops  
- 🧠 AI workflow automation  
- 📊 Large-scale generation tracking  

---

## 🔄 End-to-End Workflow

1. Add a **Prompt** in Google Sheets  
2. Set `Status = pending`  
3. Runner script:
   - Claims row → `processing`
   - Sends workflow to ComfyUI REST API
   - Waits for image completion
4. Image is uploaded to **AWS S3**
5. Sheet updates:
   - `Status = done`
   - `Output URL`
   - `Preview = IMAGE("url")`
   - Optional timestamps
6. Errors (if any) are written back to the Sheet

---

## 🏗 Architecture

Google Sheets (Queue)  
⬇  
Python Runner  
⬇  
ComfyUI REST API (Local / Pegasus GPU)  
⬇  
AWS S3 (Storage Layer)  
⬇  
Sheet updated with URL + Preview  

---

## 🧩 Tech Stack

- Python 3.9+
- gspread (Google Sheets API)
- boto3 (AWS S3)
- ComfyUI REST API
- python-dotenv
- ThreadPoolExecutor (parallel workers)

---

## 📊 Required Sheet Headers

Create a Google Sheet with the following headers in row 1:

| Header        | Required | Description |
|---------------|----------|------------|
| Prompt        | ✅ | Text prompt sent to ComfyUI |
| Status        | ✅ | pending → processing → done / error |
| Output URL    | ✅ | S3 image URL |
| Preview       | ✅ | =IMAGE("url") auto preview |
| Started at    | Optional | Timestamp |
| Finished at   | Optional | Timestamp |
| Error         | Optional | Error message |

⚠ Column order does not matter — updates are header-based.

---

## ⚙️ Setup

### 1️⃣ Clone & Install

```bash
git clone https://github.com/<yourusername>/comfyui-google-sheets-pipeline.git
cd comfyui-google-sheets-pipeline
pip install -r requirements.txt
```

---

### 2️⃣ Google Sheets Setup

- Create a Google Cloud **Service Account**
- Download the JSON key file (DO NOT commit it)
- Share your Google Sheet with the service account email (Editor access)

Set:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/service-account.json"
export SPREADSHEET_ID="your_google_sheet_id"
```

---

### 3️⃣ AWS Setup

Configure AWS credentials using:
- Environment variables
- AWS CLI profile
- IAM role (recommended for HPC / EC2)

Required:

```bash
export S3_BUCKET="your-bucket-name"
export AWS_REGION="us-east-1"
```

⚠ For previews to work:
- Either make S3 objects public
- Or implement pre-signed URLs

---

### 4️⃣ ComfyUI Setup

Start ComfyUI with API enabled:

```bash
export COMFY_API="http://127.0.0.1:8188"
```

Export your workflow as **API format** and set:

```bash
export IMAGE_WORKFLOW_JSON="workflow_image.json"
export PROMPT_NODE_ID="16"
export INPUT_KEY="text"
```

---

## ▶ Running the Pipeline

### One-Shot Mode (process pending rows once)

```bash
python runner.py
```

---

### Daemon Mode (continuous polling + parallel workers)

```bash
export DAEMON=1
export POLL_SECONDS=3
export MAX_WORKERS=2
export BATCH_CLAIM=4

python runner.py
```

---

## 🔐 Security Notes

Never commit:
- Service account JSON
- .env files
- AWS credentials

Add to `.gitignore`:

```
.env
*.json
service-account*.json
```

If credentials were accidentally committed:
- Rotate Google service account keys immediately
- Rotate AWS keys
- Remove file from git history

---

## 🧪 Designed for Research & Scale

This pipeline supports:

- Batch prompt experimentation  
- Reproducible generation logs  
- HPC-based inference  
- Automated parameter testing  
- Scalable parallel processing  
- AI workflow orchestration  

---

## 🔜 Coming Soon

- Automatic parameter logging (seed, cfg, steps)
- Prompt templating engine
- Auto-optimization loop
- Secure pre-signed S3 URLs
- Dockerized deployment
- Multi-workflow support (image + video)
- Evaluation metrics logging

---

## 🧠 Purpose

This project builds a lightweight orchestration layer between:
- Structured data (Google Sheets)
- Generative AI engines (ComfyUI)
- Scalable cloud storage (AWS S3)

It enables reproducible, trackable, and automatable AI experimentation — locally or on HPC infrastructure.

---

## 📄 License

MIT License
