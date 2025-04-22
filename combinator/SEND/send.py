import os
import time
import subprocess
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from keras import layers
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER, RF24_2MBPS, RF24_PA_HIGH

# Run shell script first
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
subprocess.run(["bash", "./aes.sh", "xcrypt"])

# Image cleanup function
def remove_corrupt_images(folder):
    count_removed = 0
    for root, _, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with Image.open(filepath) as img:
                    img.verify()
            except Exception as e:
                print(f"Deleting corrupt image: {filepath} — {e}")
                os.remove(filepath)
                count_removed += 1
    print(f"\n✅ Cleanup complete — {count_removed} file(s) removed.")

# Run this function
remove_corrupt_images('/Users/willa/Documents/oseniordesignalgorithm/Death Star')

# Dataset path setup
base_dir = '/Users/willa/Documents/oseniordesignalgorithm/Death Star'  # Change to your dataset path
dog_dir = os.path.join(base_dir, 'DeathStar')
cat_dir = os.path.join(base_dir, 'DeathStarRed')

# Check directory existence
if not os.path.exists(cat_dir) or not os.path.exists(dog_dir):
    raise FileNotFoundError("Dataset directories not found!")

# Check dataset balance
cat_count = len(os.listdir(cat_dir))
dog_count = len(os.listdir(dog_dir))
print(f"Cats: {cat_count}, Dogs: {dog_count}")

# Initialize ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.1)
test_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.1)

train_data = train_datagen.flow_from_directory(
    base_dir, target_size=(200, 200), batch_size=100, class_mode='binary', subset='training')

test_data = test_datagen.flow_from_directory(
    base_dir, target_size=(200, 200), batch_size=100, class_mode='binary', subset='validation')

# Model building
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Train the model
history = model.fit(train_data, epochs=21, validation_data=test_data)

# Plot training history
history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss']].plot()
history_df.loc[:, ['accuracy', 'val_accuracy']].plot()
plt.show()

# Save the Model for later
model.save("Find_The_DeathStar.keras")

# Load trained model
# new_model = tf.keras.models.load_model('Find_The_DeathStar.keras')

# Test a sample image
test_image = image.load_img('/Users/willa/Documents/oseniordesignalgorithm/Death Star/DeathStarRed/DS_2.png', target_size=(200, 200))
plt.imshow(test_image)
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
test_image = test_image / 255.0  # Ensure normalization

# Predict
test_result = model.predict(test_image)
print(f"Prediction score: {test_result[0][0]}")
if test_result[0][0] >= 0.5:
    print("NormalDeathStar")
else:
    print("Weakspot")


# Fine-tuning with VGG19
base_model = VGG19(input_shape=(200, 200, 3), include_top=False, weights='imagenet')
base_model.trainable = False  # Freeze base model

inputs = keras.Input(shape=(200, 200, 3))
x = preprocess_input(inputs)
x = base_model(x, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
outputs = Dense(1, activation='sigmoid')(x)

model = keras.Model(inputs, outputs)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fine-tune with VGG19
history_vgg = model.fit(train_data, epochs=5, validation_data=test_data)

# Evaluate performance
loss, acc = model.evaluate(test_data)
print(f"Test Accuracy: {acc:.2%}")

# AES encryption
subprocess.run(["bash", "./aes.sh", "zcrypt"])

# NRF24L01 communication setup
radio = RF24(22, 0)  # CE = GPIO22, CSN = CE0 on SPI bus 0: /dev/spidev0.0 

def generate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    checksum = md5_hash.hexdigest()
    print(f"MD5 checksum: {checksum}")
    return checksum

# Set up radio
def setup():
    if not radio.begin():
        print("Radio hardware not responding")
        return
    
    address = [b"1Node", b"2Node"]  # Addresses for communication
    radio.setChannel(0x60)  # Set channel 
    radio.setPALevel(RF24_PA_HIGH)  # Power Amplifier level
    radio.setDataRate(RF24_2MBPS)  # Data rate
    radio.setAutoAck(True)  # Enable auto acknowledgment
    radio.openWritingPipe(address[0])  # Address to send to (1Node)
    radio.enableDynamicPayloads()  # Enable dynamic payloads
    radio.enableAckPayload()  # Enable acknowledgment payload
    radio.printPrettyDetails()  # Print radio details
    radio.stopListening()  # Stop listening to switch to TX mode
    
    print("Radio setup complete")
    print(f"Radio Driver: {RF24_DRIVER}")
    print(f"Is chip connected? {radio.isChipConnected()}")
    print(f"Power level: {radio.getPALevel()}")
    print(f"Channel: {radio.getChannel()}")
    print(f"Data rate: {radio.getDataRate()}")
    
# Send message
def send_message(chunks):
    for chunk_index, chunk in enumerate(chunks):
        print(f"Sending chunk {chunk_index + 1}/{len(chunks)}: {chunk}")
        radio.flush_tx()
        result = radio.write(chunk)
        if result:
            print(f"Chunk {chunk_index + 1} sent successfully.")
        else:
            print(f"Chunk {chunk_index + 1} failed to send.")
        time.sleep(0.1)  # Adjust delay as needed

# Main loop
setup()

# Example of sending message
while True:
    # For this example, you would prepare your message chunks here
    # chunks = prepare_chunks()  # You should define the message chunks
    # send_message(chunks)
    time.sleep(1)
