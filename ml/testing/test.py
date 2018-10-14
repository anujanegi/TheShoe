import tensorflow as tf
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import os

models=[]

#load models
users = os.listdir('../src/Models')
for user in users:
    for file_ in os.listdir('../src/Models/'+user):
        if ".h5" in file_:
            filepath = "../src/Models/"+user+"/"+file_
            model = tf.keras.models.load_model(filepath, custom_objects=None,compile=True)
            models.append(model)

array = np.asarray([-1.2895996094,0.2153320313,9.4100097656,-0.0805999756,0.013458252,0.5881256104])
array = np.expand_dims(array, axis=0)

for model in models:
    Walk, Jog, Kick, Jump, Idle = model.predict(array)[0]
    label = (Walk, Jog, Kick, Jump, Idle)
    print(label)
