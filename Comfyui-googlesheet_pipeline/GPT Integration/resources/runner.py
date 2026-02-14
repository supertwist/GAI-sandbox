# runner.py — ComfyUI -> S3 -> Google Sheets (header-safe, no ACLs)
import os, time, json
from typing import Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional .env support
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Google Sheets (modern auth)
import gspread
from google.oauth2.service_account import Credentials

# HTTP + AWS S3
import requests
import boto3
from botocore.exceptions import ClientError
def a1_col(n: int) -> str:

    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

# ========= CONFIG / ENV =========
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")                     # REQUIRED
SHEET_NAME = None                                                      # None = first sheet
GOOGLE_CREDS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "gcp-creds.json")

COMFY_API = os.environ.get("COMFY_API", "http://127.0.0.1:8188")       # ComfyUI API (local)
IMAGE_WORKFLOW_JSON = os.environ.get("IMAGE_WORKFLOW_JSON", "workflow_image.json")
PROMPT_NODE_ID = os.environ.get("PROMPT_NODE_ID", None)                # e.g. "16"
INPUT_KEY = os.environ.get("INPUT_KEY", "text")                        # e.g. "text", "string", "input"
# Concurrency / daemon knobs
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "2"))       # how many prompts to run in parallel
POLL_SECONDS = float(os.environ.get("POLL_SECONDS", "3.0")) # how often to check the sheet
BATCH_CLAIM = int(os.environ.get("BATCH_CLAIM", "4"))       # how many rows to claim per cycle

POLL_INTERVAL = 2.0
TIMEOUT_SEC = 1200

S3_BUCKET = os.environ.get("S3_BUCKET")                                # REQUIRED
AWS_REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
S3_PREFIX = os.environ.get("S3_PREFIX", "comfyui/")                    # prefix in bucket
# =================================


# ---------- Sheets helpers ----------
def google_client():
    if not SPREADSHEET_ID:
        raise RuntimeError("SPREADSHEET_ID env var not set.")
    if not os.path.exists(GOOGLE_CREDS_FILE):
        raise RuntimeError(f"Google creds file not found: {GOOGLE_CREDS_FILE}")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(GOOGLE_CREDS_FILE, scopes=scopes)
    return gspread.authorize(creds)

def open_sheet(gc):
    sh = gc.open_by_key(SPREADSHEET_ID)
    return sh.worksheet(SHEET_NAME) if SHEET_NAME else sh.sheet1

def headers_map(ws):
    headers = ws.row_values(1)
    return {h: i + 1 for i, h in enumerate(headers) if h}

def get_pending_rows(ws):
    """
    Returns list of (row_idx, row_dict) for rows with Status='pending'.
    Uses header names instead of positional unpacking.
    """
    data = ws.get_all_records()  # list of dicts keyed by header row
    out = []
    for i, row in enumerate(data, start=2):   # data starts at row 2
        status = str(row.get("Status", "")).strip().lower()
        if status == "pending":
            out.append((i, row))
    return out

#def update_row(ws, row_idx, updates: dict):
  #  hmap = headers_map(ws)
   # for k, v in updates.items():
  #      col = hmap.get(k)
 #       if col:
#            ws.update_cell(row_idx, col, v)
# at the very start of process_row, after you compute prompt_text
   # update_row(ws, row_idx, {"Status": "processing",
   #                      "Started at": time.strftime("%Y-%m-%d %H:%M:%S")})

# ... right before the final set to done:
   # updates = {
    #   "Status": "done",
   #    "Output URL": url,
  #     "Preview": f'=IMAGE("{url}")',
 #      "Finished at": time.strftime("%Y-%m-%d %H:%M:%S")
#     }
#    update_row(ws, row_idx, updates)

def update_row(ws, row_idx, updates: dict):
    """
    Update cells by header name using a single values.batchUpdate call.
    Silently skips headers that don't exist.
    Includes retries for 429s.
    """
    hmap = headers_map(ws)
    data = []
    for k, v in updates.items():
        col = hmap.get(k)
        if not col:
            continue
        # build A1 range for a single cell
        col_letter = a1_col(col)
        rng = f"{ws.title}!{col_letter}{row_idx}"
        data.append({"range": rng, "values": [[v]]})
    if not data:
        return

    body = {"valueInputOption": "USER_ENTERED", "data": data}

    # Exponential backoff for 429s
    backoff = 1.0
    for attempt in range(6):  # ~1+2+4+8+16+32s worst-case
        try:
            ws.spreadsheet.values_batch_update(body)
            return
        except gspread.exceptions.APIError as e:
            if "429" in str(e):
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

def claim_pending_rows(ws, limit=BATCH_CLAIM):
    """
    Find up to `limit` rows with Status='pending' and immediately flip them to 'processing'
    so we don't process the same row twice if multiple loops overlap.
    Returns list of (row_idx, row_dict) that were claimed.
    """
    pending = get_pending_rows(ws)
    to_claim = pending[:limit]
    if not to_claim:
        return []
    for row_idx, _row in to_claim:
        # mark now to avoid race with next poll
        update_row(ws, row_idx, {"Status": "processing"})
    return to_claim
def worker_task(args):
    ws, row_idx, row = args
    try:
        # process_row already sets Status and writes URL/Preview; safe to call
        process_row(ws, row_idx, row)
    except Exception as e:
        update_row(ws, row_idx, {"Status": f"error: {str(e)[:150]}"})

# ---------- ComfyUI helpers ----------
def load_workflow(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def inject_prompt(wf: dict, prompt_text: str,
                  node_id: Optional[str] = PROMPT_NODE_ID,
                  input_key: str = INPUT_KEY) -> dict:
    """
    Requires workflow exported as 'Save (API format)': top-level {"prompt": {...}, "client_id": "..."} or {"prompt": {...}}
    """
    # Normalize to wf["prompt"] existence
    if "prompt" not in wf:
        # Accept a bare node dict and wrap it
        wf = {"prompt": wf}
    if node_id:
        if node_id not in wf["prompt"]:
            raise ValueError(f"Node id {node_id} not found in workflow JSON.")
        wf["prompt"][node_id]["inputs"][input_key] = prompt_text
        return wf
    # auto-find first string input with given key
    for nid, node in wf["prompt"].items():
        inputs = node.get("inputs", {})
        if isinstance(inputs.get(input_key), str):
            inputs[input_key] = prompt_text
            return wf
    raise ValueError(f"No node with a string '{input_key}' input found. Set PROMPT_NODE_ID or change INPUT_KEY.")

def comfy_submit_and_wait(payload: dict, poll_interval=POLL_INTERVAL, timeout=TIMEOUT_SEC) -> dict:
    # Ensure outer payload has "prompt"
    if "prompt" not in payload and payload:
        payload = {"prompt": payload}
    r = requests.post(f"{COMFY_API}/prompt", json=payload, timeout=60)
    r.raise_for_status()
    prompt_id = r.json()["prompt_id"]

    t0 = time.time()
    while True:
        h = requests.get(f"{COMFY_API}/history/{prompt_id}", timeout=60)
        if h.status_code == 200:
            hist = h.json()
            entry = hist.get(prompt_id, hist)  # some builds return nested by id, some directly
            outputs = entry.get("outputs", {})
            if outputs:
                return outputs
        if time.time() - t0 > timeout:
            raise TimeoutError("ComfyUI generation timed out.")
        time.sleep(poll_interval)

def extract_first_image_meta(outputs: dict) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Return (filename, subfolder, type) from the first available image output.
    """
    for _, out in outputs.items():
        imgs = out.get("images", [])
        if imgs:
            it = imgs[0]
            return it.get("filename"), it.get("subfolder"), it.get("type")
    raise ValueError("No images found in outputs. Ensure your workflow ends with a Save Image node.")

def fetch_image_bytes(filename: str, subfolder: Optional[str], ftype: Optional[str]) -> bytes:
    """
    Download the generated file from ComfyUI /view (local).
    """
    params = {"filename": filename}
    if subfolder:
        params["subfolder"] = subfolder
    if ftype:
        params["type"] = ftype
    r = requests.get(f"{COMFY_API}/view", params=params, timeout=120)
    r.raise_for_status()
    return r.content


# ---------- S3 helpers (no ACLs; use bucket policy for public read) ----------
def guess_content_type(name: str) -> str:
    n = name.lower()
    if n.endswith(".png"): return "image/png"
    if n.endswith(".jpg") or n.endswith(".jpeg"): return "image/jpeg"
    if n.endswith(".webp"): return "image/webp"
    return "application/octet-stream"

def s3_upload_bytes(bucket: str, key: str, data: bytes, content_type: str = "image/png") -> str:
    if not bucket:
        raise RuntimeError("S3_BUCKET env var not set.")
    s3 = boto3.client("s3", region_name=AWS_REGION)
    # Do NOT pass ACL when Object Ownership=Bucket owner enforced (ACLs disabled)
    s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    return f"https://{bucket}.s3.{AWS_REGION}.amazonaws.com/{key}"


# ---------- Orchestration per row ----------
def process_row(ws, row_idx: int, row: dict):
    # Read needed fields by name; missing fields default harmlessly
    prompt_text = str(row.get("Prompt", "")).strip()
    if not prompt_text:
        update_row(ws, row_idx, {"Status": "error: Empty prompt"})
        return

    update_row(ws, row_idx, {"Status": "processing"})

    try:
        # 1) Load and inject prompt into the workflow
        wf = load_workflow(IMAGE_WORKFLOW_JSON)
        wf = inject_prompt(wf, prompt_text)

        # 2) Submit to ComfyUI and wait
        outputs = comfy_submit_and_wait(wf)

        # 3) Get filename/subfolder/type from outputs
        filename, subfolder, ftype = extract_first_image_meta(outputs)

        # 4) Fetch the image bytes from /view
        blob = fetch_image_bytes(filename, subfolder, ftype)
        ctype = guess_content_type(filename)

        # 5) Build S3 key (prefix / optional subfolder / timestamp + filename)
        ts = time.strftime("%Y%m%d-%H%M%S")
        key_parts = [S3_PREFIX.strip("/")]
        if subfolder:
            key_parts.append(subfolder.strip("/"))
        key_parts.append(f"{ts}_{filename}")
        key = "/".join([p for p in key_parts if p])

        # 6) Upload to S3 and write back to sheet
        url = s3_upload_bytes(S3_BUCKET, key, blob, content_type=ctype)
        updates = {"Status": "done", "Output URL": url, "Preview": f'=IMAGE("{url}")'}
        update_row(ws, row_idx, updates)

    except Exception as e:
        update_row(ws, row_idx, {"Status": f"error: {str(e)[:150]}"})

def main():
    gc = google_client()
    ws = open_sheet(gc)

    pending = get_pending_rows(ws)
    if not pending:
        print("No pending rows.")
        return

    for row_idx, row in pending:
        print(f"Processing row {row_idx} ...")
        process_row(ws, row_idx, row)
        time.sleep(0.3)

if __name__ == "__main__":
    main()

