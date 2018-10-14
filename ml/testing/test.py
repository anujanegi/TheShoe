from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import os

models=[]

#load models
users = os.listdir('../src/Models')
for file_ in os.listdir('../src/Models/'+users):
    if ".h5" in file_:
        model = model.load_model("../src/"+file_)
        models.append(model)

array = np.asarray([1.4953613281,-8.7496582031,-1.4283691406,0.093460083,-0.5468536377,-0.0892730713])
array = np.expand_dims(array, axis=0)

for model in models:
    Walk, Jog, Kick, Jump, Idle = model.predict(array)[0]
    label = (Walk, Jog, Kick, Jump, Idle)
    print(label)
