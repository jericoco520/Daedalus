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

def chunk_file(file_path):
    '''
    Splits a file into 32-byte chunks with metadata.

    Args:
        file_path (str): The path to the file to be chunked.

    Returns:
        list: A list of 32-byte chunks (bytearrays).
    '''
    # Initialize an empty list to hold the chunks
    all_chunks = []
    
    # Open the folder
    file = pth.Path(file_path).resolve()
    
    # Check if the folder exists
    if not file.is_file():
        print(f"Error: {file} is not a valid file")
        return []
            
    print(f"Processing file: {file}")
    
    # Read the file in binary mode
    with open(file, 'rb') as f:
        chunk_index = 0
        while True:
            # Read 24 bytes of data
            data = f.read(24)
            
            if chunk_index == 0:
                print(f"First 24 bytes: {data}")
                
            if not data: # End of file
                break
            
            # Add metadata: chunk index
            metadata = struct.pack("I", chunk_index)   # 4 bytes for chunk index
            identifier = b'FILE'  # 4 bytes for future use
            
            # Combine metadata and data into 32-byte chunk
            chunk = metadata + identifier + data
            all_chunks.append(chunk)
            
            chunk_index += 1
    
    print(f"Total chunks created from folder: {len(all_chunks)}")
    return all_chunks

def reassemble_file(chunks, output_path):
    '''
    Description:
        Writes a list of bytes (chunks) into output file (output_path)
    
    Parameters:
        chunks (list[bytes]): A list of bytes to re-order after transmission
        output_path (str): The path to output file
        
    Returns:
        None
    '''
    # Sort chunks by key = chunk index
    chunks.sort(key =
                lambda chunk:
                    struct.unpack("I", chunk[:4])[0])
    
    # Write the file data to the output file
    with open(output_path, 'wb') as f:
        for chunk in chunks:
            print(f"Writing in {chunk}")
            f.write(chunk[8:])
    
# # Example usage
# chunked_file = chunk_file("zcrypt/image/test.zip")
# print(f"Size of chunked file : {len(chunked_file) * 32} bytes")

# # Example: Access the first chunk
# if chunked_file:
#     print(f"First chunk: {chunked_file[0]}")

# print(f"Reassembling chunks ...")

# reassemble_file(chunked_file, "test.zip")

# with open("test.zip", 'rb') as f:
#     data = f.read(5)
#     print(f"First 5 bytes: {data}")

def chunk_dir_png(folder_path):
    # Initialize an empty list to hold the chunks
    all_chunks = []
    
    # Open the folder
    folder = pth.Path(folder_path).resolve()
    
    # Check if the folder exists
    if not folder.is_dir():
        print(f"Error: {folder} is not a valid file")
        return []
            
    print(f"Processing file: {folder}")
    
    # Iterate through all RNG files in the folder by index
    for image_index, image_file in enumerate(folder.glob("*.png")):
        print(f"Processing image {image_index}")
        
        # Use the pack_image function to chunk the image
        image_chunks = pack_image(image_file, image_index)
        
        # Append the chunks to the all_chunks list
        all_chunks.extend(image_chunks)
        
    print(f"Total chunks created from folder: {len(all_chunks)}")
    return all_chunks