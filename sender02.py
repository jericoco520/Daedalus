import time
from pyRF24 import RF24, RF24_PA_LOW    # Module for NRF24L01

radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0

def setup():
    if not radio.begin():
        print("Radio hardware not responding")
        return

    radio.setPALevel(RF24_PA_LOW)
    radio.openWritingPipe(b'1Node')  # Address to send to
    radio.stopListening()  # Set as transmitter

    # Debugging information
    print("Radio setup complete")
    print(f"Is chip connected? {radio.isChipConnected()}")
    print(f"Power level: {radio.getPALevel()}")
    print(f"Channel: {radio.getChannel()}")
    print(f"Data rate: {radio.getDataRate()}")
    
def send_message():
    message = "Hello Pi 2!"
    print(f"Sending: {message}")
    if radio.write(message.encode()):
        print("Transmission successful")
    else:
        print("Transmission failed")

setup()

while True:
    send_message()
    time.sleep(1)
