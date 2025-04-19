import time
from packImage import reassemble_file
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS, RF24_PA_HIGH

# SPI and CE assignments for 4 radios
SPI_CONFIG = [
    {'spi_bus': 0, 'ce_pin': 22, 'channel': 0x76},
    {'spi_bus': 1, 'ce_pin': 6,  'channel': 0x77},
    {'spi_bus': 3, 'ce_pin': 23, 'channel': 0x78},
    {'spi_bus': 5, 'ce_pin': 25, 'channel': 0x79},
]

# Initialize one radio
radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0

def setup():
    '''
    Description:
        Initializes a radio and set configuration
    
    Parameters:
        None
        
    Returns:
        None
    '''    
    # Turn on radio
    if not radio.begin():
        raise RuntimeError("Radio hardware not responding")
    
    channel = SPI_CONFIG[0]['channel']

    print("Setting Radio Configuration")
    # Set configuration
    radio.setChannel(0x76)
    radio.setPALevel(RF24_PA_HIGH)
    radio.setDataRate(RF24_2MBPS)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openReadingPipe(1, b'1Node')
    radio.startListening()
    
    # Print radio information
    print("Radio setup complete")
    radio.printPrettyDetails()

def receive_message(received_chunks):
    '''
    Description:
        Receives and stores a file transmission
    
    Parameters:
        received_chunks (list): A list to store the received chunks.

    Returns:
        bool: True if the end-of-transmission signal is received, false
        otherwise
    '''
    while radio.available():
        # Get payload size
        payload_size = radio.getDynamicPayloadSize()
        
        #Read the payload as binary data
        received = radio.read(payload_size)
        
        # Add the received chunk to the buffer
        received_chunks.append(received)

        # Check for end-of-transmission signal (optional)
        for byte in received:
            if received[byte] == b'END':
                print("End of transmission signal received")
            return True  # Signal to stop receiving
        
    return False


def main():
    setup()

    # List to hold received chunks
    received_chunks = []
    
    print("Waiting for chunks...")
    while True:
        # Receive chunks
        end_of_transmission = receive_message(received_chunks)
        
        # Stop receiving if end-of-transmission signal is received
        if end_of_transmission:
            break

        time.sleep(0.1)
    
    # Reassemble the file from the received chunks
    output_file = "reassembled_file.zip"
    print(f"Reassembling file into: {output_file}")
    reassemble_file(received_chunks, output_file)

    print(f"File reassembled successfully: {output_file}")

if __name__ == "__main__":
    main()

