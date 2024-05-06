import keras.layers
import keras.utils
import tensorflow as tf
import keras
from keras.layers import Flatten, Dense, Input
import keras_vggface
from keras_vggface.vggface import VGGFace
import mtcnn
import numpy as np
import matplotlib.pyplot as mpl
from keras.utils.data_utils import get_file
import keras_vggface.utils
from PIL import Image
import os
import os.path
import wget

# vggface = VGGFace(model='vgg16')
# vggface_resnet = VGGFace(model='resnet50')
# vggface_senet = VGGFace(model='senet50')
# print(vggface.summary())
# print('Inputs: ', vggface.inputs)
# print('Outputs: ', vggface.outputs)
# wget.download('https://upload.wikimedia.org/wikipedia/commons/c/c4/Antonin_Scalia_%2847277900881%29.jpg', 
#               'public_images/scalia.jpg')
# scalia_photo = mpl.imread('public_images/scalia.jpg')
# scalia_photo.shape
# face_detector = mtcnn.MTCNN()
# face_data = face_detector.detect_faces(scalia_photo)
# # print(face_data)
# x1, y1, w, h = face_data[0]['box']
# x2, y2 = x1 + w, y1 + h
# face = scalia_photo[y1:y2, x1:x2]
# print(scalia_photo.shape)
# print(face.shape)
# mpl.imshow(scalia_photo)
# mpl.imshow(face)

train_dataset = keras.utils.image_dataset_from_directory('training',
                                                         shuffle=True,
                                                         batch_size=8,
                                                         image_size=(224,224))

data_augmentation = keras.Sequential([
    keras.layers.RandomFlip('horizontal'),
    keras.layers.RandomRotation(0.2),
])

vggface_resnet_base = VGGFace(model='resnet50',
                              include_top=False,
                              input_shape=(224,224,3))

nb_class = 2 # currently 1 POI + 1 for invalid

#freeze base pretrained model
vggface_resnet_base.trainable = False
last_layer = vggface_resnet_base.get_layer('avg_pool').output

#build the new model
inputs = tf.keras.Input(shape=(224,224,3))
x = data_augmentation(inputs)
x = vggface_resnet_base(x)
x = Flatten(name='flatten')(x)
out = Dense(nb_class, name='classifier')(x)
custom_vgg_model = keras.Model(inputs,out)

custom_vgg_model.compile(optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),
                         loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                         metrics=['accuracy'])
history = custom_vgg_model.fit(train_dataset, epochs=20)



prob_model = keras.Sequential([
    custom_vgg_model,
    tf.keras.layers.Softmax()
])

prob_model.summary()
custom_vgg_model.summary()

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
