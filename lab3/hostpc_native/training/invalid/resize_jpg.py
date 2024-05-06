from PIL import Image
import os
import glob
import tensorflow
import mtcnn
import matplotlib.pyplot as mpl
# NOTE MUST BE EXECUTED IN IMAGE DIR!

# fetch all images in pwd
file_names = []
pwd = os.getcwd()
for name in glob.glob(pwd + '/*.jpg'):
    print(name)
    file_names.append(name)

# resize each file
face_detector = mtcnn.MTCNN()
for img_path in file_names:
    # img = Image.open(img_path)
    img = mpl.imread(img_path)
    
    face_data = face_detector.detect_faces(img)
    if face_data:
        x1, y1, w, h = face_data[0]['box']
        x2, y2 = x1 + w, y1 + h
        face = img[y1:y2, x1:x2]

        face_image = Image.fromarray(face)
        face_image = face_image.resize((224, 224), Image.Resampling.LANCZOS)
        face_image.save(img_path)

