# -*- coding: utf-8 -*-
"""cat and dog classifier .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1owdVdnLeq3eKTTqrT6rttcqXKhcUiRWc
"""

!mkdir -p ~/ .kaggle
!cp /content/kaggle.json ~/.kaggle/

!kaggle datasets download -d tongpython/cat-and-dog

import zipfile

zip_path = '/content/cat-and-dog.zip'  # Replace with the correct path to your zip file

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('/content')  # Extract the contents to the '/content' directory
    print('The contents of the zip file have been extracted successfully.')
except Exception as e:
    print(f"Error extracting the zip file: {e}")

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout

#generator
train_ds = keras.utils.image_dataset_from_directory(
      directory = '/content/training_set' ,
      labels = 'inferred' ,
      label_mode = 'int' ,
      batch_size = 30 ,
      image_size=(256,256)
)

validation_ds = keras.utils.image_dataset_from_directory(
      directory = '/content/test_set' ,
      labels = 'inferred' ,
      label_mode = 'int' ,
      batch_size = 30 ,
      image_size=(256,256)
)

#Normalize
def process(image,label):
    image = tf.cast(image/255. ,tf.float32)
    return image,label

traiin_ds = train_ds.map(process)
validation_ds = validation_ds.map(process)

# Create CNN Model

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(train_ds, epochs=10, validation_data=validation_ds)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

import cv2

test_img = cv2.imread('/content/Dog image.jpg')

plt.imshow(test_img)

test_img.shape

test_img = cv2.resize(test_img,(256,256))

test_input = test_img.reshape((1,256,256,3))

model.predict(test_input)

test_img = cv2.imread('/content/cat image.jpg')

plt.imshow(test_img)

test_img.shape

test_img = cv2.resize(test_img,(256,256))

test_input = test_img.reshape((1,256,256,3))

model.predict(test_input)