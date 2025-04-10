# This module holds the function to take a 1024 x 1024 PNG image
# and pack it into 32 byte payloads for transmission over the nRF24L01 radio.

# The image is split into 32 byte chunks held in a list or an array.

# Function: pack_image(image_path)
# Parameters:
#     image_path (str): The path to the PNG image file.
# Returns: a list of bytearrays, each containing 32 bytes of image data.

def pack_image(image_path):
    print(f"Packing image: {image_path}")