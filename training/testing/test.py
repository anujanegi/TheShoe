import tensorflow as tf
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import os

models=[]
labels=[]

#load models
users = os.listdir('../src/Models')
for user in users:
    for file_ in os.listdir('../src/Models/'+user):
        if "modeltest.h5" in file_:
            filepath = "../src/Models/"+user+"/"+file_
            print(filepath)
            model = tf.keras.models.load_model(filepath, custom_objects=None,compile=True)
            models.append(model)


# sample test data for user1 walk
array = [2.33515625, 6.1297851563, 9.321484375, 0.1459472656, 0.3831115723, 0.5825927734]
array = np.asarray(array)
array = np.expand_dims(array, axis=0)

# sample test for gait biometrichon3
for model in models:
    Walk, Jog, Kick, Jump, Idle = model.predict(array)[0]
    label = (Walk, Jog, Kick, Jump, Idle)
    # labels = labels + label
    print("Walk:"+str(Walk)+" Jog:"+str(Jog)+" Kick:"+str(Kick)+" Jump:"+str(Jump)+" Idle:"+str(Idle))
