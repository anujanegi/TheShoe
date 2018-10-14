import numpy as np
import tensorflow as tf
from keras.datasets import reuters
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers


def def_model(num_of_features) :

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(100, activation='relu', input_shape=(num_of_features, )))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(5, activation='softmax'))
    return model

def compile_model(model):
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

def fit_model(model, trainX, trainY, testX, testY):
    model.fit(np.array(trainX), np.array(trainY), epochs=200, verbose=1, batch_size=10, validation_data=(np.array(testX), np.array(testY)))
    return model

def evaluate(model, X, Y):
	scores = model.evaluate(np.array(X),np.array(Y))
	print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
