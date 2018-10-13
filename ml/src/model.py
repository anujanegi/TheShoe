import numpy as np
from keras.datasets import reuters
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers


def def_model(num_of_features) :

    model = models.Sequential()
    model.add(layers.Dense(units=100, activation='relu', input_shape=(num_of_features,)))
    model.add(layers.Dense(units=50, activation='relu'))
    model.add(layers.Dense(units=5, activation='softmax'))

    return model

def compile_model(model):
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

def fit_model(model, trainX, trainY, testX, testY):
    model.fit(trainX, trainY, epochs=200, verbose=0, batch_size=10, validation_data=(testX, testY))
    return model

def evaluate(model, X, Y):
	scores = model.evaluate(X,Y)
	print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
