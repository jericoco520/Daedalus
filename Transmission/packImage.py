from email.mime import image
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
#     a list of bytearrays, each containing 32 bytes of image data.
'''
def pack_image(image_path, image_index: int):
    print(f"Packing image: {pth.Path(image_path).resolve()}")
    
    # Open the image using PIL
    img = PIL.Image.open(image_path)
    print(f"Original image size: {img.size}, mode: {img.mode}")
    
    # Convert the image to RGBA format
    img = img.convert("RGBA")
    print(f"Image mode after conversion: {img.mode}")
    
    # Resize the image to 1024 x 1024 pixels
    img = img.resize((1024, 1024))
    print(f"Image size after resizing: {img.size}")
    
    # # DEBUGGING Inspect the first few pixels 
    # pixels = list(img.getdata())
    # print(f"First 10 pixels: {pixels[500000:500010]}")
    
    # Convert the image to a byte array
    img_data = img.tobytes()
    
    # DEBUGGING
    # print(f"First 100 bytes of img_data: {img_data[500000:500010]}")
    
    # Calculate the number of chunks needed
    num_chunks = len(img_data) // 32 + (1 if len(img_data) % 32 else 0)
    print(f"Number of chunks: {num_chunks}")
    
    # Create a list to hold the chunks
    chunks = []
    
    # Split the image data into 32 byte chunks
    for i in range(num_chunks):
        start = i * 32
        end = start + 32
        chunk = img_data[start:end]
        
        # Pad the chunk with zeros if it's less than 32 bytes
        if len(chunk) < 32:
            chunk += b'\x00' * (32 - len(chunk))
        
        # Add metadata: image index and chunk index
        metadata= struct.pack("HH", image_index, i)
        # Append the chunk and metadata to the list
        chunks.append(metadata + chunk)

    print(f"Packed {len(chunks)} chunks of image {image_index}.")
    return chunks   # Return the list of chunks containing 32 bytes each

# Function: chunk_file(file_path)
# Parameters:
#     folder_path (str): The path to the folder to be packed.
# Returns: a list of bytearrays, each containing 32 bytes of file data.
def chunk_file(folder_path):
    # Initialize an empty list to hold the chunks
    all_chunks = []
    
    # Open the folder
    folder = pth.Path(folder_path).resolve()
    print(f"Processing folder: {folder}")
    
    # Check if the folder exists
    if not folder.is_dir():
        print(f"Error: {folder} is not a valid directory")
        return []
            
    # Iterate through all RNG files in the folder
    for image_index, image_file in enumerate(folder.glob("*.png")):
        print(f"Processing image {image_index}: {image_file}")
        
        # Use the pack_image function to chunk the image
        image_chunks = pack_image(image_file, image_index)
        
        # Append the chunks to the all_chunks list
        all_chunks.extend(image_chunks)
        
    print(f"Total chunks created from folder: {len(all_chunks)}")
    return all_chunks
    
    

# Example usage
image_data = pack_image("Eart.png")     # ==> Transmit each chunk of image data

