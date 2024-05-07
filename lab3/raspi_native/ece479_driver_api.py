import time
import os
import io
import tensorflow
import tflite_runtime.interpreter as tflite
from capture_image import *
from detect_and_crop import *
from image_to_jpeg import *
from mtcnn import MTCNN
from PIL import Image
from telegramAPI import *
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import numpy as np
import asyncio

TOKEN = '7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM'
chat_idx = -4135478636
name = ""

def main():
    #setup
    print("Setup Tensorflow...")
    mtcnn = MTCNN()
    interpreter = tflite.Interpreter(model_path='res50net_lite_num3.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print("Begin Polling Camera...")
    while True:
        #raspi-cam grab 768by1024 RGB img
        image = capture_image()
        
        #mtcnn to detect face
        #crop img with detected face to mtcnn bounding box
        cropped_image = detect_and_crop(mtcnn, image)
        
        #save output jpeg with timestamp
        if cropped_image is not None:
            print("Face detected...")
            img_data = image_to_jpeg(cropped_image, f"capture_{int(time.time())}")
            #bot.send_photo(chat_id=-4135547836, photo=img_data)
            #bot.send_message(chat_id=-4135547836, text='Is this a known person?')
            img_data.show()
            img_nparr = np.array(img_data)
            
            #run inference
            img_data_float = img_nparr[:,:,:].astype(np.float32)
            img_batch = np.zeros(shape=(1,224,224,3), dtype=np.float32)
            img_batch[0] = img_data_float
            interpreter.set_tensor(input_details[0]['index'], img_batch)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print(output_data)

            name = recogonizeGuest(output_data)

            asyncio.run(sendName(name))
            print('Sleep...')
            time.sleep(1)
            print('Awake...')

if __name__ == "__main__":
    main()
