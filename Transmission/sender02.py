import time
from pyrf24 import RF24 , RF24_PA_LOW, RF24_DRIVER   # Module for NRF24L01

radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0

# Set up radio
def setup():
    # Initialize radio and check if responding
    if not radio.begin():
        print("Radio hardware not responding")
        return

    # Set radio parameters
    radio.setChannel(0x76)               # Set channel to 0x76
<<<<<<< HEAD
    radio.setPALevel(RF24.RF24_PA_LOW)   # Power Amplifier level
=======
    radio.setPALevel(RF24_PA_LOW)   # Power Amplifier level
>>>>>>> main
    radio.openWritingPipe(b'1Node')      # Address to send to
    radio.printDetails()                 # Print radio details
    radio.stopListening()                # Set as transmitter
    
    # Debugging information
    print("Radio setup complete")
    print(f"Is chip connected? {radio.isChipConnected()}")  
    print(f"Power level: {radio.getPALevel()}")
    print(f"Channel: {radio.getChannel()}")
    print(f"Data rate: {radio.getDataRate()}")
    
# Send message
def send_message():
    # Create message
<<<<<<< HEAD
    message = list("Hello Pi 2!")
=======
    message = "Hello Pi 2!"
>>>>>>> main
    # Print Sending message
    print(f"Sending: {message}")
    
    # Radio send message with confirmatino of success or failure
    if radio.write(message.encode()):
        print("Transmission successful")
    else:
        print("Transmission failed")

# Main loop
setup()

# Send message every second
<<<<<<< HEAD
 while True:
     send_message()
     time.sleep(1)
=======
# while True:
#     send_message()
#     time.sleep(1)
>>>>>>> main
