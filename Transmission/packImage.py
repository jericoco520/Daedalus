import pathlib as pth
import PIL
import PIL.Image 
# This module holds the function to take a 1024 x 1024 PNG image
# and pack it into 32 byte payloads for transmission over the nRF24L01 radio.

# The image is split into 32 byte chunks held in a list or an array.

# Function: pack_image(image_path)
# Parameters:
#     image_path (str): The path to the PNG image file.
# Returns: a list of bytearrays, each containing 32 bytes of image data.
def pack_image(image_path):
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
    
    # Inspect the first few pixels
    pixels = list(img.getdata())
    print(f"First 10 pixels: {pixels[500000:500010]}")
    
    # Convert the image to a byte array
    img_data = img.tobytes()
    print(f"First 100 bytes of img_data: {img_data[500000:500010]}")
    
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
        
        # Append the chunk to the list
        chunks.append(bytearray(chunk))

    print(f"Packed {len(chunks)} chunks of image data.")
    return chunks
    
# Example usage
    
image_data = pack_image("Eart.png")

# Print the first 5 chunks
# for i in range(100000, 100100):
#     print(f"Chunk {i}: {image_data[i]}")