## for ECE479 ICC Lab2 Part3

'''
*Main Student Script*
'''

# Your works start here

# Import packages you need here
from inception_resnet import InceptionResNetV1Norm
import numpy as np
import tensorflow as tf
import os

# Create a model
model = InceptionResNetV1Norm()
model.save_weights("code/weights/inception_keras_weights.h5")  # Has been translated from checkpoint

model = InceptionResNetV1Norm()
model.load_weights("code/weights/inception_keras_weights.h5")  # Has been translated from checkpoint

# Verify the model and load the weights into the net
print(model.summary())
print()
print(len(model.layers))

# begin converting to '.tflite' file
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_resnet = converter.convert()

# write to new file
with open('quantized_resnet_model.tflite', 'wb') as f:
    f.write(tflite_resnet)
