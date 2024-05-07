import keras.layers
import keras.utils
import tensorflow as tf
import keras
from keras.layers import Flatten, Dense, Input
from keras_vggface.vggface import VGGFace
import numpy as np
import matplotlib.pyplot as mpl
import os
import os.path

train_dataset = keras.utils.image_dataset_from_directory('training',            #
                                                         shuffle=True,          # As long as 'training/' is formatted correctly
                                                         batch_size=8,          # this will import the file hierachy and classes
                                                         image_size=(224,224))  #

data_augmentation = keras.Sequential([      # This will supplemenet the much lower amount of training data
    keras.layers.RandomFlip('horizontal'),  # by adding randomness to the inputs
    keras.layers.RandomRotation(0.2),       # Greatly improving the training process
])

resnet50_base = VGGFace(model='resnet50',               # base pre-trained model
                              include_top=False,        # false; will add custom output layers
                              input_shape=(224,224,3))  # image input format

num_class = 3 # currently 2 POI + 1 for invalid

#freeze base pretrained model
resnet50_base.trainable = False
last_layer = resnet50_base.get_layer('avg_pool').output

#build the new model
inputs = tf.keras.Input(shape=(224,224,3)) # image format is 224x224 RGB
x = data_augmentation(inputs)
x = resnet50_base(x)
x = Flatten(name='flatten')(x)
out = Dense(num_class, name='classifier')(x)
custom_resnet_model = keras.Model(inputs,out)

custom_resnet_model.compile(optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),
                         loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                         metrics=['accuracy'])
history = custom_resnet_model.fit(train_dataset, epochs=20)



prob_model = keras.Sequential([
    custom_resnet_model,
    tf.keras.layers.Softmax()
])

prob_model.summary()
custom_resnet_model.summary()

pwd = os.getcwd()
samples = np.zeros(shape=(3,224,224,3))
sample = mpl.imread(pwd + '\\testing\\noah\\noahtest.jpg')
samples[0] = sample
sample = mpl.imread(pwd + '\\testing\\noah\\cattest.jpg')
samples[1] = sample
sample = mpl.imread(pwd + '\\testing\\noah\\trumptest.jpg')
samples[2] = sample
predictions = prob_model.predict(samples)
print(predictions)

converter = tf.lite.TFLiteConverter.from_keras_model(prob_model)
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_LATENCY]
tflite_model = converter.convert()
with open('res50net_lite_model.tflite', 'wb') as f:
    f.write(tflite_model)
