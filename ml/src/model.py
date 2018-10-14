import numpy as np
from keras.datasets import reuters
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers


def def_model(num_of_features) :

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(100, activation='relu', input_shape=(num_of_features,)))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(5, activation='softmax'))
    return model

def compile_model(model):
    model.compile(loss=tf.keras.losses.categorical_crossentropy,
                  optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                  metrics=[tf.keras.metrics.categorical_accuracy],)
    return model

def fit_model(model, trainX, trainY, testX, testY):
    model.train_on_batch(trainX, trainY)
    model.test_on_batch(testX, testY)
    return model

def evaluate(model, X, Y):
	scores = model.evaluate(X,Y)
	print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
