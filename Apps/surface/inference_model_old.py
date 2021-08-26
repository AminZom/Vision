"""
Inference testing model for metal surface detect and classification
"""


import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import cv2

saved_model = load_model('LG_model.h5')


# Preparing imagedata generator for test data
test_datagen = ImageDataGenerator(rescale=1. / 255,
                                  shear_range=0.2,
                                  zoom_range=0.2,
                                  horizontal_flip=True,
                                  vertical_flip=True)


# change below location to the test folder or image location
test_location = 'NEU surface defect database - test split/spoon'
# image = Image.open(test_location + '/spoon2.jpg')
# image.show()

test_generator = test_datagen.flow_from_directory(test_location,
                                                  target_size=(200, 200),
                                                  batch_size=1,
                                                  class_mode=None,
                                                  shuffle=False)

# In[ ]:


step_size_test = test_generator.n // test_generator.batch_size
print(step_size_test)
test_generator.reset()

# In[ ]:

saved_model.compile(loss='categorial_crossentropy', optimizer='adam', metrics=['acc'])
image = cv2.imread(test_location + '/In/Pitting-Corrosion.jpg')
image  = cv2.resize(image, (200,200))
results = saved_model.predict_classes(image)
print(results)
# predIndxs = saved_model.predict_generator(test_generator, steps=step_size_test, verbose=1)
# print (predIndxs)

# acc_o = np.sum(np.argmax(predIndxs, axis=1).astype('int') == test_generator.labels) / test_generator.n
# print(acc_o)