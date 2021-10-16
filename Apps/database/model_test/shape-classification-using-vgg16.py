#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import shutil
import os
from tensorflow.keras.applications import VGG16
from tensorflow.keras import models, layers
from keras.preprocessing.image import ImageDataGenerator

# os.mkdir("datasetset")
# os.mkdir(os.path.join(base_dir, 'train'))
# os.mkdir(os.path.join(base_dir, 'validation'))
# os.mkdir(os.path.join(base_dir, 'test'))

base_dir = "datasetset/"
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')


# os.mkdir(train_dir + "/circles_samples")
# os.mkdir(test_dir + "/circles_samples")
# os.mkdir(validation_dir + "/circles_samples")

data_source = "./circles_samples/"
destination = ""
train = ['drawing({}).png'.format(i) for i in range(1, 66)]
for i in train:
    src = data_source + i
    des = "datasetset/train/circles_samples/" + i
    shutil.copyfile(src, des)

validation = ['drawing({}).png'.format(i) for i in range(66, 81)]
for i in validation:
    src = data_source + i
    des = "datasetset/validation/circles_samples/" + i
    shutil.copyfile(src, des)

test = ['drawing({}).png'.format(i) for i in range(81, 101)]
for i in test:
    src = data_source + i
    des = "datasetset/test/circles_samples/" + i
    shutil.copyfile(src, des)

conv_base = VGG16(include_top=False, weights='imagenet', input_shape=(32, 32, 3))

data_gen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = data_gen.flow_from_directory(
    train_dir,
    target_size=(32, 32),
    color_mode='rgb',
    batch_size=6
)
validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(32, 32),
    batch_size=6,
    color_mode='rgb'
)

# In[15]:


model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
# model.add(layers.Dense(1, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

conv_base.trainable = False


model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

# In[18]:


history = model.fit_generator(
    train_generator,
    steps_per_epoch=11,
    epochs=8,
    validation_data=validation_generator,
    validation_steps=3
)

# In[19]:
# Solved by using tensorflow=2.3, cudnn=7.6.5 and cudatoolkit=10.1

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()

# In[20]:


test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(32, 32),
    batch_size=20,
    color_mode='rgb'
)

# In[21]:


test_loss, test_acc = model.evaluate_generator(test_generator)
print('test acc:', test_acc)

# In[ ]:
