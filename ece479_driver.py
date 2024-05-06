import time
import os
import io
import tensorflow
from capture_image import *
from detect_and_crop import *
from image_to_jpeg import *
from mtcnn import MTCNN
from PIL import Image

#setup
mtcnn = MTCNN()

#main
while True:
    #raspi-cam grab 768by1024 RGB img
    image = capture_image()
    
    #mtcnn to detect face
    #crop img with detected face to mtcnn bounding box
    cropped_image = detect_and_crop(mtcnn, image)
    
    #save output jpeg with timestamp
    if cropped_image is not None:
        img_data = image_to_jpeg(cropped_image, f"capture_{int(time.time())}")
        img_data.show()
    
    #run inference
    #TODO
    
    
    #upload to raspi-host
    #TODO
        
