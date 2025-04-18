# ============================== IMPORTS ==============================
import os  # file system operations
import sys  # system args and control
import time  # sleep/delay
import glob  # pattern-based file search
import gzip  # not used in current version
import hashlib  # MD5 checksum
import shutil  # copying and zipping
import zipfile  # unzip functionality
import multiprocessing  # parallel processing
from pathlib import Path  # object-based file paths
from Crypto.Cipher import AES  # encryption
from Crypto.Random import get_random_bytes  # secure keygen
from reedsolo import RSCodec  # error correction
from github import Github  # GitHub API
from subprocess import run  # run shell commands
from extract_inside_red import extract_and_crop_inside_red  # red image cropper
from PIL import Image, ImageTk  # image handling
import tkinter as tk  # GUI window
from RF24 import RF24, RF24_PA_LOW  # nRF24L01 radio
import random  # random for channel hopping
from collections import defaultdict  # channel success/failure tracking

# =========================== CONFIGURATION ===========================
# SPI and CE assignments for 4 radios
SPI_CONFIG = [
    {'spi_bus': 0, 'ce_pin': 22, 'channel': 0x76},
    {'spi_bus': 1, 'ce_pin': 6,  'channel': 0x77},
    {'spi_bus': 3, 'ce_pin': 23, 'channel': 0x78},
    {'spi_bus': 5, 'ce_pin': 25, 'channel': 0x79},
]

GITHUB_TOKEN = "<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>"  # GitHub access token
GITHUB_REPO = "<username>/<repo-name>"  # target GitHub repo
HOLADATA_PATH = os.path.expanduser("~/Desktop/holodata")  # folder to send
ZIP_PATH = os.path.expanduser("~/Desktop/holodata.zip")  # zip output
DEATH_STAR_GIF = "/mnt/data/Death_Star_explosion.gif"  # explosion animation

CHUNK_SIZE = 20  # bytes per radio chunk
RS_BYTES = 10  # Reed-Solomon FEC bytes
AES_KEY = b'0123456789ABCDEF'  # Fixed 128-bit AES key for repeatable testing  # 128-bit AES key
PIPE_SEND = b"1Node"  # TX pipe
PIPE_RECV = b"2Node"  # RX pipe
CHANNEL_LIST = list(range(0x00, 0x7E))  # full list of usable channels

# Store success/failure stats for each channel
channel_quality = defaultdict(lambda: {'success': 0, 'fail': 0})

# =============================== UTILS ===============================
def run_pre_hooks():
    # run any data prep scripts before transmission
    run(["python3", "ImageTrain.py"])
    run(["python3", "run.py"])

def zip_holodata():
    # zip up the holodata folder
    shutil.make_archive(ZIP_PATH.replace(".zip", ""), 'zip', HOLADATA_PATH)

def calculate_md5(path):
    # calculate md5 for any file
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def encrypt_chunk(chunk):
    # AES encryption using EAX mode
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(chunk)
    return cipher.nonce + tag + ciphertext

def decrypt_chunk(blob):
    # decrypt AES blob back to original
    nonce, tag, ciphertext = blob[:16], blob[16:32], blob[32:]
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def stardust():
    # Death Star explosion popup window
    root = tk.Tk()
    root.title("Death Star Explosion")
    gif = Image.open(DEATH_STAR_GIF)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass

    lbl = tk.Label(root)
    lbl.pack()
    def animate(idx=0):
        lbl.config(image=frames[idx])
        root.after(50, animate, (idx + 1) % len(frames))
    animate()
    root.mainloop()

# ========================== RADIO SETUP ==============================
def setup_radios():
    # Create and initialize radio interfaces per SPI/CE config
    radios = []
    for i, cfg in enumerate(SPI_CONFIG):
        radio = RF24(cfg['ce_pin'], cfg['spi_bus'])
        if not radio.begin():
            raise RuntimeError(f"Radio failed to start on SPI{cfg['spi_bus']}, CE{cfg['ce_pin']}")
        radio.setPALevel(RF24_PA_LOW)
        radio.setRetries(5, 15)
        radio.setChannel(cfg['channel'])
        radio.setPayloadSize(32)
        radio.openWritingPipe(PIPE_RECV)
        radio.openReadingPipe(1, PIPE_SEND)
        radio.stopListening()
        radios.append({'radio': radio, 'channel': cfg['channel'], 'spi': cfg['spi_bus'], 'ce': cfg['ce_pin'], 'index': i})
    return radios

# ================ SMART FREQUENCY HOPPING ===========================
def hop_channel(radio_dict):
    # Choose better channel based on fewer failures
    scored = sorted(CHANNEL_LIST, key=lambda ch: (channel_quality[ch]['fail'] - channel_quality[ch]['success']))
    for candidate in scored:
        if candidate != radio_dict['channel']:
            radio_dict['radio'].setChannel(candidate)
            radio_dict['channel'] = candidate
            print(f"[HOP] SPI{radio_dict['spi']} CE{radio_dict['ce']} -> {hex(candidate)}")
            break

# ============================= TRANSMIT =============================
def transmitter():
    run_pre_hooks()
    zip_holodata()
    checksum = calculate_md5(ZIP_PATH)
    rsc = RSCodec(RS_BYTES)
    radios = setup_radios()

    # Read data from zip and divide evenly
    with open(ZIP_PATH, 'rb') as f:
        file_data = f.read()

    chunk_size = len(file_data) // len(radios)
    chunks = [file_data[i * chunk_size:(i + 1) * chunk_size] for i in range(len(radios))]
    chunks[-1] += file_data[len(radios) * chunk_size:]

    def tx_task(radio_dict, chunk):
        radio = radio_dict['radio']
        coded = rsc.encode(chunk)
        encrypted = encrypt_chunk(coded)
        radio.stopListening()
        for i in range(0, len(encrypted), 32):
            payload = encrypted[i:i + 32].ljust(32, b'\x00')
            retries = 0
            while retries < 5:
                if radio.write(payload):
                    channel_quality[radio_dict['channel']]['success'] += 1
                    break
                retries += 1
                channel_quality[radio_dict['channel']]['fail'] += 1
                hop_channel(radio_dict)
                time.sleep(0.01)

    jobs = []
    for r, c in zip(radios, chunks):
        p = multiprocessing.Process(target=tx_task, args=(r, c))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()

# ============================= RECEIVE ==============================
def receiver():
    radios = setup_radios()
    rsc = RSCodec(RS_BYTES)
    manager = multiprocessing.Manager()
    results = manager.dict()

    def rx_task(radio_dict):
        radio = radio_dict['radio']
        idx = radio_dict['index']
        radio.startListening()
        buffer = bytearray()
        while True:
            if radio.available():
                buffer += radio.read(32)
                if len(buffer) > CHUNK_SIZE + 32:
                    channel_quality[radio_dict['channel']]['success'] += 1
                    break
            else:
                channel_quality[radio_dict['channel']]['fail'] += 1
                hop_channel(radio_dict)
                time.sleep(0.01)
        try:
            decoded = decrypt_chunk(buffer)
            results[idx] = rsc.decode(decoded)
        except Exception as e:
            print(f"[RX{idx}] Error: {e}")

    jobs = []
    for r in radios:
        p = multiprocessing.Process(target=rx_task, args=(r,))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()

    with open(ZIP_PATH, 'wb') as f:
        for i in sorted(results):
            f.write(results[i])

    if calculate_md5(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, 'r') as z:
            z.extractall(HOLADATA_PATH)

    run(["python3", "run.py"])
    extract_and_crop_inside_red(HOLADATA_PATH, output_pattern="cropped_image_{}.png")

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    for file in glob.glob(os.path.join(HOLADATA_PATH, "cropped_image_*.png")):
        with open(file, 'rb') as f:
            content = f.read()
        repo.create_file(f"holodata/{os.path.basename(file)}", "auto upload", content, branch="main")

    stardust()

# ============================ ENTRY ===============================
# Run as either transmitter or receiver depending on command line argument
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "receiver"
    if mode == "transmitter":
        transmitter()
    else:
        # Default behavior: run receiver if no argument is given
        receiver()
