from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2

#load model
json_file = open('../src/model.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("../src/model.h5")

array = np.asarray([1.9810546875, -2.9715820313, 8.6108886719, 0.123815918, -0.185723877,0.538180542])
array = np.expand_dims(array, axis=0)
Walk, Jog, Kick, Jump, Idle = model.predict(array)[0]
label = (Walk, Jog, Kick, Jump, Idle)
print(label)