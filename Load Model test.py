import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import os
import cv2
import shutil
import re
import matplotlib.image as mpimg
import subprocess
from PIL import Image
from tensorflow import keras
from keras import layers
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input


#Load trained model
new_model = tf.keras.models.load_model('Find_The_Diamond.keras')


# Test a sample image
#test_image = image.load_img('/Users/willa/Documents/oseniordesignalgorithm/dog-vs-cat/cat/cat.1.jpg', target_size=(200, 200))
test_image = image.load_img('/Users/willa/Documents/oseniordesignalgorithm/Mr.Oreo.png', target_size=(200, 200))

plt.imshow(test_image)
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
test_image = test_image / 255.0  # Ensure normalization

# Predict
test_result = new_model.predict(test_image)
print(f"Prediction score: {test_result[0][0]}")
if test_result[0][0] >= 0.5:
    print("Dog")
else:
    print("Cat")


## Image sorting
def sort_images_with_model(source_dir, dest_dir, model):
    """Uses a trained model to sort images into 'cat' folder based on prediction.
    Resizes images to 200x200 for prediction, saves as 1024x1024 if classified as cat."""

    os.makedirs(dest_dir, exist_ok=True)
    cat_dir = os.path.join(dest_dir, 'cat')
    os.makedirs(cat_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)

        if os.path.isfile(source_path):
            try:
                # Load and preprocess for model (200x200, normalized)
                img = image.load_img(source_path, target_size=(200, 200))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0

                # Predict
                prediction = model.predict(img_array)
                if prediction[0][0] < 0.5:  # Cat detected
                    # Reload and resize to 1024x1024 for saving
                    with Image.open(source_path) as orig_img:
                        resized_img = orig_img.resize((1024, 1024))
                        dest_path = os.path.join(cat_dir, filename)
                        resized_img.save(dest_path)
                        print(f"Saved cat: {filename}")
                else:
                    print(f"Skipped dog: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
        ##if os.path.isfile(source_path):
         ##   if re.search(r"cat", filename, re.IGNORECASE):
        ##        dest_path = os.path.join(dest_dir, 'cat', filename)
         ##       shutil.copy2(source_path, dest_path)
            

# Example usage
source_directory = 'D:/Bunny'
destination_directory = '/Users/willa/Documents/oseniordesignalgorithm/sorted/'
sort_images_with_model(source_directory, destination_directory, new_model)

# Image put into folder



##End image sorting

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
#history_vgg = model.fit(train_data, epochs=5, validation_data=test_data)

#Evaluate performance
#loss, acc = model.evaluate(test_data)
#print(f"Test Accuracy: {acc:.2%}")