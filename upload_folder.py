#!/usr/bin/env python3
import os
import requests
import sys
from PIL import Image
import tempfile

RESIZE_TO = (512, 512)  # width x height

BASE       = "http://10.17.155.230/imagegallery/pi_uploads"
GET_URL    = f"{BASE}/images.php"
POST_URL   = f"{BASE}/upload.php"
FOLDER     = r"C:\Users\swebs\OneDrive\Pictures\TPImages"
ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}

def upload_file(path: str):
    filename = os.path.basename(path)
    ext = filename.rsplit('.', 1)[-1].lower()
    mime_map = {
        'jpg':  'image/jpeg',
        'jpeg': 'image/jpeg',
        'png':  'image/png',
        'gif':  'image/gif',
        'webp': 'image/webp',
        'bmp':  'image/bmp'
    }
    mime = mime_map.get(ext, 'application/octet-stream')

    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            img = img.resize(RESIZE_TO, Image.LANCZOS)
            with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
                temp_path = tmp.name
                img.save(temp_path)
    except Exception as e:
        print(f"✗ Failed to resize {filename}: {e}")
        return

    with open(temp_path, 'rb') as f:
        files = {'image': (filename, f, mime)}
        resp = requests.post(POST_URL, files=files, timeout=30)

    os.remove(temp_path)

    if resp.ok:
        data = resp.json()
        if data.get('status') == 'success':
            print(f"✓ Uploaded {filename} → {data['path']}")
        else:
            print(f"✗ Server error for {filename} →", data.get('message'))
    else:
        print(f"✗ HTTP {resp.status_code} for {filename}")

def upload_folder(folder: str):
    print(f"Scanning folder: {folder}")
    for entry in os.listdir(folder):
        full = os.path.join(folder, entry)
        ext = os.path.splitext(entry)[1].lower()
        if os.path.isfile(full) and ext in ALLOWED_EXT:
            upload_file(full)
    print("Done uploading batch.")

def fetch_and_print_list():
    resp = requests.get(GET_URL, timeout=10)
    if resp.ok:
        lst = resp.json()
        print("\n=== All Images in Database ===")
        for img in lst:
            print(" •", img.get('path'))
    else:
        print("Failed to fetch images list:", resp.status_code)

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else FOLDER
    if not os.path.isdir(folder):
        print("Error: folder not found:", folder)
        sys.exit(1)

    upload_folder(folder)
    fetch_and_print_list()
