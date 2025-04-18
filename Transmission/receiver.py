import time
from packImage import reassemble_file
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS, RF24_PA_HIGH

radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0
global received_chunks

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
    
    # Set configuration
    radio.setChannel(0x60)
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

def receive_message():
    '''
    Description:
        Receives and stores a file transmission
    
    Parameters:
        None
        
    Returns:
        None
    '''

    while radio.available():
        # Get payload size
        payload_size = radio.getDynamicPayloadSize()
        
        #Read the payload as binary data
        received = radio.read(payload_size)
        
        # Add the received chunk to the buffer
        received_chunks.append(received)

        # Check for end-of-transmission signal (optional)
        if received == b"END":
            print("End of transmission signal received")
            return True  # Signal to stop receiving
        
    return False


def main():
    setup()

    print("Waiting for chunks...")
    while True:
        # Receive chunks
        end_of_transmission = receive_message()
        
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

