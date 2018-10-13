from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import os

models=[]
#load model
files = os.listdir('../src/')
for file_ in files:
    if ".json" in file_:
        json_file = open("../src/"+file_, 'r')
        model_json = json_file.read()
        json_file.close()
        model = model_from_json(model_json)
        model.load_weights("../src/"+file_.split(".")[0]+".h5")
        models.append(model)

array = np.asarray([1.4953613281,-8.7496582031,-1.4283691406,0.093460083,-0.5468536377,-0.0892730713])
array = np.expand_dims(array, axis=0)

for model in models:
    Walk, Jog, Kick, Jump, Idle = model.predict(array)[0]
    label = (Walk, Jog, Kick, Jump, Idle)
    print(label)
