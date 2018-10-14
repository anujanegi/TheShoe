import numpy as np
import pickle
import tensorflow as tf
from keras.models import load_model
from data import *
from model import *

np.random.seed(399)
trainX, trainY, testX, testY = load_data()
# print(trainX.shape, trainY.shape)
model = fit_model(compile_model(def_model(6)), trainX, trainY, testX, testY)
evaluate(model, trainX, trainY)

filename = "./Models/user2/model.h5"
tf.keras.models.save_model(model, filename)
converter = tf.contrib.lite.TocoConverter.from_keras_model_file(filename)
tflite_model = converter.convert()
open("./Models/user2/model.tflite", "wb").write(tflite_model)
