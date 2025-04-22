import time
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS, RF24_PA_HIGH

radio = RF24(22, 0)  # CE=GPIO22, CSN=SPI0 CS0

def setup():
    if not radio.begin():
        raise RuntimeError("Radio hardware not responding")
    
    radio.setChannel(0x76)
    radio.setPALevel(RF24_PA_HIGH)
    radio.setDataRate(RF24_2MBPS)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openReadingPipe(1, b'1Node')
    radio.startListening()
    
    print("Radio setup complete")
    radio.printPrettyDetails()

def receive_message():
    while radio.available():
        # Get payload size
        payload_size = radio.getDynamicPayloadSize()
        
        # Read the payload
        received = radio.read(payload_size)
        print(f"Received: {received}")

setup()

while True:
    receive_message()
    time.sleep(0.1)