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
#from telegram.ext import Updater, CommandHandler
#from telegram import Bot

#def unrecogonizedGuest(update, context):
#            text = update.message.text
#            # Check if the message contains a specific word or phrase
#            if 'yes' in text.lower():
#                update.message.reply_text('Letting in guest')
#            elif 'no' in text.lower():
#                update.message.reply_text('Not letting unknown person in')

#setup
mtcnn = MTCNN()
interpreter = tflite.Interpreter(model_path='res50net_lite_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#bot = Bot(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')
#updater = Updater(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')

#dispatcher = updater.dispatcher
#dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unrecogonizedGuest))

#updater.start_polling()
# updater.idle()
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
        #file_name = int(time.time())
        #bot.send_photo(chat_id=-4135547836, photo=img_data)
        #bot.send_message(chat_id=-4135547836, text='Is this a known person?')
        img_data.show()
        img_nparr = np.array(img_data)
        
        #run inference
        #TODO
        img_data_float = img_data[:,:,:].astype(np.float32)
        interpreter.set_tensor(input_details[0]['index'], img_data_float)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        print(output_data)
    
    
    #upload to raspi-host
    #TODO
        
