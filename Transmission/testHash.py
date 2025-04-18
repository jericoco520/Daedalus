import hashlib
import os

def generate_md5(file_path):
    """
    Generates the MD5 checksum of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: MD5 checksum of the file.
    """
    md5_hash = hashlib.md5()
    
    # Update hash by chunks of file
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    checksum = md5_hash.hexdigest()
    
    # Print checksum
    print(f"MD5 checksum: {checksum}")
    return checksum

# Test
original = os.stat("zcrypt/image/test.zip")
sent = os.stat("test.zip")
 
checksum = generate_md5("zcrypt/image/test.zip")
newChecksum = generate_md5("test.zip")

print(f"Checksum pre-tranmission: {checksum}")
print(f"Size of original: {original.st_size}")
print(f"Checksum post-transmission: {newChecksum}")
print(f"Size of sent: {sent.st_size}")

# Read original file
with open("zcrypt/image/test.zip", 'rb') as f:
    data = f.read()
    data = list(data)
    sizeData = len(data)
    print(f"Last 10 bytes of original file: {data[ sizeData - 32:sizeData ]}")
    
with open("test.zip", 'rb') as f:
    data = f.read()
    data = list(data)
    sizeData = len(data)
    print(f"Last 10 bytes of received file: {data[ sizeData - 32:sizeData ]}")