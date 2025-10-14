# 🧠 ComfyUI + Google Sheets + AWS S3 Pipeline

This project connects **Google Sheets** to **ComfyUI** (a local Stable Diffusion workflow engine) with HPC cluster(Peagasus) and uploads generated images to **AWS S3**, automatically updating the Sheet with live previews.

## 🚀 Workflow
1. A user adds a **prompt** in Google Sheets and marks status as `pending`.
2. The script detects pending rows.
3. ComfyUI generates the image locally.
4. The image is uploaded to **AWS S3**.
5. The Sheet updates with:
   - ✅ Status: `done`
   - 🌐 Output URL
   - 🖼️ Preview (auto image display)

## 🧩 Tech Stack
- Python
- Google Sheets API (via gspread)
- AWS S3 (via boto3)
- ComfyUI REST API
- Environment Variables (`dotenv`)

## ⚙️ Setup
```bash
git clone https://github.com/<yourusername>/comfyui-google-sheets-pipeline.git
cd comfyui-google-sheets-pipeline
pip install -r requirements.txt
