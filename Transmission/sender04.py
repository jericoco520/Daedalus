import time
from pyrf24 import RF24 , RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS, RF24_PA_HIGH   # Module for NRF24L01

radio = RF24(22, 0)  # CE = GPIO22, CSN = CE0 on SPI bus 0: /dev/spidev0.0 

# Set up radio
def setup():
    # Initialize radio and check if responding
    if not radio.begin():
        print("Radio hardware not responding")
        return

    address = [b"1Node", b"2Node"]       # Addresses for communication
    #radio.open_tx_pipe(address[0])       # Open TX pipe with address[0]
    #radio.open_rx_pipe(1, address[1])    # Open RX pipe with address[1]
    radio.setChannel(0x60)               # Set channel 
    radio.setPALevel(RF24_PA_HIGH)       # Power Amplifier level
    radio.setDataRate(RF24_2MBPS)        # Data rate
    radio.setAutoAck(True)               # Enable auto acknowledgment
    radio.openWritingPipe(address[0])    # Address to send to (1Node)
    radio.enableDynamicPayloads()        # Enable dynamic payloads
    radio.enableAckPayload()             # Enable acknowledgment payload
    radio.enable_dynamic_ack()           # Enable dynamic acknowledgment
    #radio.listen = False                 # Set radio in TX mode
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
def send_message():
    # Create message
    message = "Hello Pi 2!"
    buffer = bytearray(message, 'utf-8')  # Convert message to bytearray
    
    # Limit the buffer size to 32 bytes
    if len(buffer) > 32:
        buffer = buffer[:32]
        
    # Print Sending message
    print(f"Sending: {message}")
    
    # Load payload to TX Pipe
    radio.flush_tx()  # Flush TX buffer
    #radio.start_write(buffer)
    result = False
    result = radio.write_fast(buffer)  # Send the message ## write_fast worked for 3 sends
    # Radio send message with confirmatino of success or failure
    if result:
        print("Transmission successful")
    else:
        print(f"Transmission failed with result: ", result)

# Main loop
setup()

# Send message every second
while True:
    send_message()
    time.sleep(1)
