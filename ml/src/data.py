import pandas
import numpy as np
from keras.utils import np_utils
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# csv file format
# x, y, z, ADCx,  ADCy,  ADCz, label

def load_data():
    dataset = pandas.read_csv("../dataset/user1/DataWalk.csv", header=None)
    data = dataset.values
    coordinates = data[:,0:3].astype(float)
    X = data[:,0:6].astype(float)
    Y = data[:,6].astype(int)

    X = np.array(X, dtype = "float")
    Y = np.array(Y, dtype = "int")

    (trainX, testX, trainY, testY) = train_test_split(X, Y, test_size=0.25, random_state=10)

    # set numeber of classes
    trainY = to_categorical(trainY, num_classes=5)
    testY = to_categorical(testY, num_classes=5)
    return trainX, trainY, testX, testY
