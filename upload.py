import os
import requests

# 1) Match this to wherever you put the pi_uploads folder
BASE       = "http://10.17.155.230/imagegallery/pi_uploads"
GET_URL    = f"{BASE}/images.php"
POST_URL   = f"{BASE}/upload.php"
IMAGE_PATH = r"C:\Users\Sam\Downloads\Arlecchino.png"

# 2) Verify the GET endpoint
r = requests.get(GET_URL, timeout=5)
print("GET images.php →", r.status_code, r.text)

# 3) Perform the POST upload
with open(IMAGE_PATH, 'rb') as f:
    files = {
        'image': (
            os.path.basename(IMAGE_PATH),  # e.g. "Arlecchino.png"
            f,
            'image/png'                     # correct MIME for a .png
        )
    }
    resp = requests.post(POST_URL, files=files, timeout=10)
    print("POST upload.php →", resp.status_code, resp.text)
