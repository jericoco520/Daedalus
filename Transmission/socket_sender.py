import socket
import time
from packImage import chunk_file

def send_file(file_path, host, port):
    """
    Sends a file in chunks over a TCP socket.

    Args:
        file_path (str): Path to the file to send.
        host (str): IP address of the receiver.
        port (int): Port number to connect to.

    Returns:
        None
    """
    # Chunk the file
    print(f"Chunking file: {file_path}")
    chunks = chunk_file(file_path)
    if not chunks:
        print("Failed to chunk the file. Exiting.")
        return

    print(f"Total chunks to send: {len(chunks)}")

    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {host}:{port}...")
        s.connect((host, port))
        print("Connected.")

        # Send each chunk
        for chunk_index, chunk in enumerate(chunks):
            print(f"Sending chunk {chunk_index + 1}/{len(chunks)}...")
            s.sendall(chunk)  # Send the chunk
            time.sleep(0.01)  # Small delay to avoid overwhelming the receiver

        # Send end-of-transmission signal
        end_signal = b"END"
        s.sendall(end_signal)
        print("End-of-transmission signal sent.")

    print("File sent successfully.")

if __name__ == "__main__":
    # Path to the file to send
    file_path = "zcrypt/image/test.zip"

    # Receiver's IP address and port
    host = "10.16.164.218"  # Replace with the receiver's IP address
    port = 12345          # Port to connect to

    send_file(file_path, host, port)