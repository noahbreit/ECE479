# -*- coding: utf-8 -*-
## for ECE479 ICC Lab2 Part3

'''
*Keras definition for inception resnet v1*
'''

# Import all packages
from resnet_block import *
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Definition for the Inception ResNet Structure starts here
def InceptionResNetV1Norm(input_shape=(160, 160, 3),
                          classes=512,
                          dropout_keep_prob=0.8,
                          weights_path=None):

    # DO NOT TOUCH
    inputs = Input(shape=input_shape)
    # Example of how to use conv2d_bn
    # Note: this is also part of the netowrk, do not delete it
    x = conv2d_bn(inputs,
                  32,
                  3,
                  strides=2,
                  padding='valid',
                  name='Conv2d_1a_3x3')
    ############################################

    # Preprocess inputs by MaxPooling2D
    ## TO DO Step 1 : Finish the implementation for preprocessing with given parameters
    # Please name all layers properly to make it easy for your debugging
    # Your code goes here
    # inputs = Input(shape=(77, 77, 32))
    x = conv2d_bn(x,
                  64,                # TODO: confirm
                  3,
                  strides=1,
                  padding='same',
                  name='Conv2d_1b_3x3')

    # inputs = Input(shape=(77, 77, 64))
    # x = MaxPooling2D(
    #                  pool_size=(2,2),
    #                  strides=2,
    #                  name='MaxPool_1a_3x3')(x)
    x = MaxPooling2D(3, 
                     strides=2, 
                     padding='valid', 
                     name='MaxPool_1a_3x3')(x)

    # inputs = Input(shape=(38, 38, 64))
    x = conv2d_bn(x,
                  80,
                  1,
                  strides=1,
                  padding='valid',
                  name='Conv2d_1c_3x3')
    
    # inputs = Input(shape=(38, 38, 80))
    x = conv2d_bn(x,
                  192,
                  3,
                  strides=1,
                  padding='valid',
                  name='Conv2d_1d_3x3')

    # inputs = Input(shape=(36, 36, 192))
    x = conv2d_bn(x,
                  256,
                  3,
                  strides=2,
                  padding='valid',
                  name='Conv2d_1e_3x3')
    ##############################################

    # 5x Inception-ResNet-A block:
    ## TO DO Step 2 : Finish the implementation for Inception-A block with given parameters
    # Please name all blocks properly to make it easy for your debugging
    # Hint : Use for loop to instantiate multiples reception blocks
    # Your code goes here
    scale = 0.17
    min_block_idx = 1
    max_block_idx = 5
    block_type = 'Inception_block_a'

    for idx in range(min_block_idx, max_block_idx + 1):
        x = resnet_block(x, scale, idx, block_type)

    ###############################################

    # Mixed 6a (Reduction-A block):
    channel_axis = 1 if K.image_data_format() == 'channels_first' else 3
    name_fmt = partial(generate_layer_name, prefix='Mixed_6a')
    branch_0 = conv2d_bn(x,
                         384,
                         3,
                         strides=2,
                         padding='valid',
                         name=name_fmt('Conv2d_1a_3x3', 0))
    branch_1 = conv2d_bn(x, 192, 1, name=name_fmt('Conv2d_0a_1x1', 1))
    branch_1 = conv2d_bn(branch_1, 192, 3, name=name_fmt('Conv2d_0b_3x3', 1))
    branch_1 = conv2d_bn(branch_1,
                         256,
                         3,
                         strides=2,
                         padding='valid',
                         name=name_fmt('Conv2d_1a_3x3', 1))
    branch_pool = MaxPooling2D(3,
                               strides=2,
                               padding='valid',
                               name=name_fmt('MaxPool_1a_3x3', 2))(x)
    branches = [branch_0, branch_1, branch_pool]
    x = Concatenate(axis=channel_axis, name='Mixed_6a')(branches)

    # 10x Inception-ResNet-B block:
    ## TO DO Step 3 : Finish the implementation for Inception-B block with given parameters
    # Please name all blocks properly to make it easy for your debugging
    # Hint : Use for loop to instantiate multiples reception blocks
    # Your code goes here
    scale = 0.1
    min_block_idx = 1
    max_block_idx = 10
    block_type = 'Inception_block_b'

    for idx in range(min_block_idx, max_block_idx + 1):
        x = resnet_block(x, scale, idx, block_type)

    ###############################################

    # Mixed 7a (Reduction-B block)
    name_fmt = partial(generate_layer_name, prefix='Mixed_7a')
    branch_0 = conv2d_bn(x, 256, 1, name=name_fmt('Conv2d_0a_1x1', 0))
    branch_0 = conv2d_bn(branch_0,
                         384,
                         3,
                         strides=2,
                         padding='valid',
                         name=name_fmt('Conv2d_1a_3x3', 0))
    branch_1 = conv2d_bn(x, 256, 1, name=name_fmt('Conv2d_0a_1x1', 1))
    branch_1 = conv2d_bn(branch_1,
                         256,
                         3,
                         strides=2,
                         padding='valid',
                         name=name_fmt('Conv2d_1a_3x3', 1))
    branch_2 = conv2d_bn(x, 256, 1, name=name_fmt('Conv2d_0a_1x1', 2))
    branch_2 = conv2d_bn(branch_2, 256, 3, name=name_fmt('Conv2d_0b_3x3', 2))
    branch_2 = conv2d_bn(branch_2,
                         256,
                         3,
                         strides=2,
                         padding='valid',
                         name=name_fmt('Conv2d_1a_3x3', 2))
    branch_pool = MaxPooling2D(3,
                               strides=2,
                               padding='valid',
                               name=name_fmt('MaxPool_1a_3x3', 3))(x)
    branches = [branch_0, branch_1, branch_2, branch_pool]
    x = Concatenate(axis=channel_axis, name='Mixed_7a')(branches)

    # 5x Inception-ResNet-C block:
    ## TO DO Step 4 : Finish the implementation for Inception-B block with given parameters
    # Please name all blocks properly to make it easy for your debugging
    # Hint : Use for loop to instantiate multiples reception blocks
    # Your code goes here
    scale = 0.2
    min_block_idx = 1
    max_block_idx = 5
    block_type = 'Inception_block_c'

    for idx in range(min_block_idx, max_block_idx + 1):
        x = resnet_block(x, scale, idx, block_type)

    ###############################################

    # Final Inception Block
    x = resnet_block(x,
                     scale=1.,
                     block_idx=6,
                     block_type='Inception_block_c',
                     activation=None)


    # Classification block
    ## TO DO Step 5 : Apply Global Average pooling + Dropout layers
    # Please name all blocks properly to make it easy for your debugging
    # x = # Your code goes here (do not modify the variable name assigned to)
    # x = # Your code goes here (do not modify the variable name assigned to)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(rate=(1.0 - dropout_keep_prob))(x)     # TODO: confirm


    ## DO NOT TOUCH
    # (BottleNeck blcok with Normalization)
    x = Dense(classes, use_bias=False, name='Bottleneck')(x)
    bn_name = generate_layer_name('BatchNorm', prefix='Bottleneck')
    x = BatchNormalization(momentum=0.995,
                           epsilon=0.001,
                           scale=False,
                           name=bn_name)(x)
    x = Lambda(K.l2_normalize, arguments={'axis': 1}, name='normalize')(x)

    # Create model
    model = Model(inputs, x, name='inception_resnet_v1')
    if weights_path is not None:
        model.load_weights(weights_path)

    return model
    #############################################################