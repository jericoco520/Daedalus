import time
import hashlib

from pyrf24 import RF24 , RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS, RF24_PA_HIGH   # Module for NRF24L01

# SPI and CE assignments for 4 radios
SPI_CONFIG = [
    {'spi_bus': 0, 'ce_pin': 22, 'channel': 0x76},
    {'spi_bus': 1, 'ce_pin': 6,  'channel': 0x77},
    {'spi_bus': 3, 'ce_pin': 23, 'channel': 0x78},
    {'spi_bus': 5, 'ce_pin': 25, 'channel': 0x79},
]

radio = RF24(22, 0)  # CE = GPIO22, CSN = CE0 on SPI bus 0: /dev/spidev0.0 

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

# Set up radio
def setup():
    # Initialize radio and check if responding
    if not radio.begin():
        print("Radio hardware not responding")
        return
    
    address = [b"1Node", b"2Node"]       # Addresses for communication
    radio.setChannel(0x60)               # Set channel 
    radio.setPALevel(RF24_PA_HIGH)       # Power Amplifier level
    radio.setDataRate(RF24_2MBPS)        # Data rate
    radio.setAutoAck(True)               # Enable auto acknowledgment
    radio.openWritingPipe(address[0])    # Address to send to (1Node)
    radio.enableDynamicPayloads()        # Enable dynamic payloads
    radio.enableAckPayload()             # Enable acknowledgment payload
    radio.printPrettyDetails()           # Print radio details
    radio.stopListening()                # Stop listening to switch to TX mode
    
    # Debugging information
    print("Radio setup complete")
    print(f"Radio Driver: {RF24_DRIVER}")
    print(f"Is chip connected? {radio.isChipConnected()}")  
    print(f"Power level: {radio.getPALevel()}")
    print(f"Channel: {radio.getChannel()}")
    print(f"Data rate: {radio.getDataRate()}")
    
# Send message
def send_message(chunks):
    '''
    Sends a list of 32-byte chunks using the NRF24L01 radio.

    Args:
        chunks (list): List of 32-byte chunks (bytearrays) to send.

    Returns:
        None
    '''
    for chunk_index, chunk in enumerate(chunks):
        # Print the chunk being sent
        print(f"Sending chunk {chunk_index + 1}/{len(chunks)}: {chunk}")

        # Flush TX buffer before sending
        radio.flush_tx()

        # Send the chunk
        result = radio.write(chunk)

        # Check if the transmission was successful
        if result:
            print(f"Chunk {chunk_index + 1} sent successfully.")
        else:
            print(f"Chunk {chunk_index + 1} failed to send.")

        # Add a small delay between transmissions
        time.sleep(0.1)  # Adjust delay as needed

# Main loop
setup()

# Send message every second
while True:
    send_message()
    time.sleep(1)
