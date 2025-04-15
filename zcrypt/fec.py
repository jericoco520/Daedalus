import hashlib

def send_data(data, socket):
	# Create a hash of the data
	data_hash = hashlib.sha256(data.encode()).hexdigest()
	socket.sendall(f"{data}|{data_hash}".encode())

# ON PI 2
# def receive_data(socket):
# 	# Receive data and hash
# 	data_with_hash = socket.recv(1024).decode()
# 	data, sent_hash = data_with_hash.split("|")

# 	# Verify the hash
# 	calculated_hash = hashlib.sha256(data.encode()).hexdigest()
    
# 	if calculated_hash == sent_hash:
#     	print("Data received correctly:", data)
# 	else:
#     	print("Data corrupted!")
