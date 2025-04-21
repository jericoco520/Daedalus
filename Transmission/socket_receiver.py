import socket
from packImage import reassemble_file

def receive_file(output_path, host, port):
    """
    Receives a file in chunks over a TCP socket and reassembles it.

    Args:
        output_path (str): Path to save the reassembled file.
        host (str): IP address to bind to.
        port (int): Port number to listen on.

    Returns:
        None
    """
    # Buffer to store received chunks
    received_chunks = []

    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port}...")
        conn, addr = s.accept()
        print(f"Connection established with {addr}.")

        with conn:
            while True:
                # Receive data in chunks
                chunk = conn.recv(32)  # Receive 32 bytes at a time
                if not chunk:
                    break
                
                # Check for end-of-transmission signal
                if chunk == b"END":
                    print("End of transmission signal received.")
                    break
                
                # Append valid chunks to the buffer
                received_chunks.append(chunk)
                print(f"Received chunk of size {len(chunk)} bytes.")

    # Reassemble the file from the received chunks
    print(f"Reassembling file into: {output_path}")
    reassemble_file(received_chunks, output_path)
    print(f"File reassembled successfully: {output_path}")

if __name__ == "__main__":
    # Path to save the reassembled file
    output_path = "reassembled_file.zip"

    # Receiver's IP address and port
    host = "10.16.164.218"  # Listen on all interfaces
    port = 8001             # Port to listen on

    receive_file(output_path, host, port)