import time
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER   # Module for NRF24L01

radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0

# Setup radio
def setup():
    if not radio.begin():
        print("Radio hardware not responding")
        return

    # Set radio parameters
    radio.setChannel(0x76)              # Set channel to 0x76
    radio.setPALevel(RF24_PA_LOW)       # Power Amplifier level
    radio.openReadingPipe(1, b'1Node')  # Address to receive from
    radio.printDetails()                # Print radio details
    radio.startListening()              # Set as receiver
    
    # Debugging information
    print("Radio setup complete")
    print(f"Is chip connected? {radio.isChipConnected()}")  
    print(f"Power level: {radio.getPALevel()}")
    print(f"Channel: {radio.getChannel()}")
    print(f"Data rate: {radio.getDataRate()}")

def receive_message():
    if radio.available():
        received = radio.read(32).decode()
        print(f"Received: {received}")
    else:
        print("No data received")

setup()


while True:
    receive_message()
    time.sleep(0.5)
