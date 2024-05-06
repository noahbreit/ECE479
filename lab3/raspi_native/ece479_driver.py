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

#from telegram.ext import Updater, CommandHandler
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

TOKEN = '7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM'
bot = Bot(token=TOKEN)
chat_id = -4125547836
#updater = Updater(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')

#dispatcher = updater.dispatcher
#dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unrecogonizedGuest))

#updater.start_polling()
# updater.idle()
#main


# async def startCommand(update, context):
#     await update.message.reply_text('Hi! Send me an image and I will save it.')

# # async def letIn(update, context):
# #     await update.message.send_message('Letting In ' + name)

# def recogonizeGuest(prob_array):

#             arr = prob_array[0]
#             maxIdx = np.argmax(arr)

#             if maxIdx == 0:

#                 return "invalid"
            
#             elif maxIdx == 1:

#                 return "Noah"

#             elif maxIdx == 2:

#                   return "Vishvesh"
            
# if __name__ == "__main__":
#     print( 'Starting bot...')
#     app = Application.builder().token(TOKEN).build()
#     # Commands
#     # app.add_handler(CommandHandler ('saveImage', saveImageHandler)) 
#     app.add_handler(CommandHandler ("start", startCommand))
#     # Errors
#     # app.add_error_handler (error)
#     # Polls the bot
#     print( 'Polling...')
#     app.run_polling(poll_interval=3)

#######################################################################################################################################################################################



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
        img_data_float = img_nparr[:,:,:].astype(np.float32)
        img_batch = np.zeros(shape=(1,224,224,3), dtype=np.float32)
        img_batch[0] = img_data_float
        interpreter.set_tensor(input_details[0]['index'], img_batch)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        print(output_data)

        
        name = recogonizeGuest(output_data)

        bot.send_message(chat_id=chat_id, text=name)



    
    
    #upload to raspi-host
    #TODO


        
