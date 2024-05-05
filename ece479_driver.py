from capture_image import *
from detect_and_crop import *
from show_bounding_box import *
import os
import io
import tensorflow
from mtcnn import MTCNN

image = capture_image()
mtcnn = MTCNN()
cropped_image, bounding_box = detect_and_crop(mtcnn, image)
show_bounding_box(cropped_image, bounding_box)
