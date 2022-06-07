import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing import text

# test to ensure tf & keras are operating nominally
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

def
