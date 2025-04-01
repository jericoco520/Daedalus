import time
from pyrf24 import RF24 , RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS   # Module for NRF24L01

radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0

# Set up radio
def setup():
    # Initialize radio and check if responding
    if not radio.begin():
        print("Radio hardware not responding")
        return

    # Set radio parameters
    radio.setChannel(0x76)               # Set channel to 0x76
    radio.setPALevel(RF24_PA_LOW)        # Power Amplifier level
    radio.setDataRate(RF24_2MBPS)        # Data rate
    radio.set_auto_ack(True)             # Enable auto acknowledgment
    radio.openWritingPipe(b'1Node')      # Address to send to
    radio.printPrettyDetails()           # Print radio details
    radio.listen = False                 # Set radio in TX mode
    
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
    
    # Pack the payload
    result = radio.write(buffer)
    # Radio send message with confirmatino of success or failure
    if result:
        print("Transmission successful")
    else:
        print(f"Transmission failed with result: ", result)

# Main loop
setup()

# Send message every second
while True:
    # Check if radio is ready
    radio.powerUp()  # Power up the radio
    radio.flush_tx()  # Clear any previous transmissions
    
    # Send message
    send_message()
    time.sleep(1)
