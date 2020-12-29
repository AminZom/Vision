"""
Inference testing model for metal surface detect and classification
"""

import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras.optimizers import SGD
import cv2

def getPredictions():
    
    saved_model = load_model('LG_model_last.h5')                        # Load trained model
    test_datagen = ImageDataGenerator(rescale=1. / 255, 
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True,
                                    vertical_flip=True)                 # Preparing imagedata generator for test data

    test_location = 'NEU surface defect database - test split/Test'     # change below location to the test folder or image location
    test_generator = test_datagen.flow_from_directory(test_location,
                                                    target_size=(200, 200),
                                                    batch_size=1,
                                                    class_mode=None,
                                                    shuffle=False)      # batches of images from the subdirectories

    step_size_test = test_generator.n // test_generator.batch_size
    #print(step_size_test)
    test_generator.reset()


    saved_model.compile(optimizer=SGD(), loss='categorical_crossentropy',
                        metrics=['accuracy'])

    img = cv2.imread('NEU surface defect database - test split/spoon/Cr/spoon2.jpg')    # To run one image at the time
    img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_AREA)
    img = np.reshape(img, [1, 200, 200, 3])     # reshape the image similar to model's input

    img = img/255.0
    results = saved_model.predict(img)      # predict the accuracy of all categories for img image
    catg = np.argmax(results)               # final category is the one with highest percentage

    predIndxs = saved_model.predict_generator(test_generator, steps=step_size_test, verbose=1)      # run this for predicting batches of 6 classes. predIndxs is a 180x6 array - 180 images for 6 different categories
    return predIndxs

    #acc_o = np.sum(np.argmax(predIndxs, axis=1).astype('int') == test_generator.labels) / test_generator.n
    #print(acc_o)