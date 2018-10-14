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

    array = [-0.1100585938,6.8858398438,11.7451660156,-0.0068786621,0.4303649902,0.734072876,
-8.5726074219,-2.5696289063,14.3171875,-0.5357879639,-0.1606018066,0.8948242188,
4.8138671875,1.7059082031,18.2212768555,0.3008666992,0.1066192627,1.1388298035,
-2.0073730469,0.9785644531,9.0463378906,-0.1254608154,0.0611602783,0.5653961182,
-2.3782226563,0.937890625,8.9338867188,-0.148638916,0.0586181641,0.5583679199,
-2.7107910156,1.3422363281,7.4552734375,-0.1694244385,0.0838897705,0.4659545898,
-0.8780761719,6.5604492188,7.0078613281,-0.0548797607,0.4100280762,0.437991333,
-19.0999511719,10.3120117188,16.80546875,-1.1937469482,0.6445007324,1.0503417969,
-1.5599609375,0.4330566406,15.2574707031,-0.0974975586,0.02706604,0.9535919189,
-1.9260253906,1.1795410156,9.1611816406,-0.1203765869,0.0737213135,0.5725738525]
    array = np.asarray(array)
    array = np.expand_dims(array, axis=0)
    print("\n")
    for model in models:
        Walk, Jog, Kick, Jump, Idle = model.predict(array)[0]
        label = (Walk, Jog, Kick, Jump, Idle)
        print(label)
