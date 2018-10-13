import numpy as np
import pickle
from keras.models import model_from_json
from data import *
from model import *

np.random.seed(399)
trainX, trainY, testX, testY = load_data()
model = fit_model(compile_model(def_model(6)), trainX, trainY, testX, testY)
evaluate(model, trainX, trainY)

model_json = model.to_json()
with open("model_user2.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model_user2.h5")
