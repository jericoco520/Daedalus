from reedsolo import RSCodec

radio.setRetries(15, 15)

rsc = RSCodec(10)
def send_data(data):
    encoded_data = rsc.encode(data.encode())
    radio.write(encoded_data)
rsc = RSCodec(10) #same codec

try:
    # Decode the received data using FEC
    decoded_data = rsc.decode(received_data)
    print("Received:", decoded_data.decode())
except:
    print("Trying again")