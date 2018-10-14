import numpy as np
import pickle
import tensorflow as tf
from keras.models import load_model
from data import *
from model import *

np.random.seed(399)
trainX, trainY, testX, testY = load_data()
# print(trainX.shape, trainY.shape)
model = fit_model(compile_model(def_model(3)), trainX, trainY, testX, testY)
evaluate(model, trainX, trainY)

filename = "model_user1.h5"
tf.keras.models.save_model(model, filename)
converter = tf.contrib.lite.TocoConverter.from_keras_model_file(keras_file)
tflite_model = converter.convert()
open("model_user1.tflite", "wb").write(tflite_model)
