import pathlib as pth
import struct
import PIL
import PIL.Image 
# This module holds the function to take a 1024 x 1024 PNG image
# and pack it into 32 byte payloads for transmission over the nRF24L01 radio.

# The image is split into 32 byte chunks held in a list or an array.
'''
# Function: pack_image(image_path)

# Parameters:
#     image_path (str): The path to the PNG image file.

# Returns: 
#     a list of bytes, each containing 24 bytes of image data and 
#     8 bytes of metadata.
'''
def pack_image(image_path, image_index: int):
    
    # Open the image using PIL
    img = PIL.Image.open(image_path)
    
    # Convert image to palette mode if not already
    if img.mode != "P":
        print(f"Converting image {image_index} to Palette Mode (P)")
        img = img.convert("P")
        print(f"Image Mode: {img.mode}")
    
    # Resize the image to 1024 x 1024 pixels
    img = img.resize((1024, 1024))
    
    # Convert the image to a byte array
    img_data = img.tobytes()
    
    # Calculate the number of chunks needed
    num_chunks = len(img_data) // 24 + (1 if len(img_data) % 24 else 0)
    
    # Create a list to hold the chunks
    chunks = []
    
    # Split the image data into 32 byte chunks
    for i in range(num_chunks):
        start = i * 24
        end = start + 24
        chunk = img_data[start:end]
        
        # Pad the chunk with zeros if it's less than 32 bytes
        if len(chunk) < 24:
            chunk += b'\x00' * (24 - len(chunk))
        
        # Add metadata: image index and chunk index
        metadata= struct.pack("II", image_index, i)
        # Append the chunk and metadata to the list
        chunks.append(metadata + chunk)

    print(f"Packed {len(chunks)} chunks of image {image_index}.\n")
    return chunks   # Return the list of chunks containing 32 bytes each

'''
# Description:
        This function will take a folder in the same directory and chunk 
        each PNG image into one list[bytes].
# Function: 
#       chunk_file(folder_path)

# Parameters:
#       folder_path (str): The path to the folder to be packed.

# Returns:
#       a list of bytes, each containing 24 bytes of image data and
#       8 bytes of metadata.
'''
def chunk_file(file_path):
    # Initialize an empty list to hold the chunks
    all_chunks = []
    
    # Open the folder
    file = pth.Path(file_path).resolve()
    
    # Check if the folder exists
    if not file.is_dir():
        print(f"Error: {file} is not a valid directory")
        return []
            
    # Iterate through all RNG files in the folder by index
    for image_index, image_file in enumerate(file.glob("*.png")):
        print(f"Processing image {image_index}")
        
        # Use the pack_image function to chunk the image
        image_chunks = pack_image(image_file, image_index)
        
        # Append the chunks to the all_chunks list
        all_chunks.extend(image_chunks)
        
    print(f"Total chunks created from folder: {len(all_chunks)}")
    return all_chunks

# Example usage
image_data = chunk_file("png_images")
print(f"Size of image_data: {len(image_data) * 32} bytes")

