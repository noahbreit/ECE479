# from telegram.ext import Updater, CommandHandler
# # from telegram import Bot, Updater
import numpy as np
# # from hostpc_native.tf_driver import *
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# bot = Bot(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')
TOKEN = '7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM'

# def unrecogonizedGuest(update, context):
#             text = update.message.text
#             # Check if the message contains a specific word or phrase
#             if 'yes' in text.lower():
#                 update.message.reply_text('Who is this?')
#                 name = update.message.text


#             elif 'no' in text.lower():
#                 update.message.reply_text('Not letting unknown person in')

async def startCommand(update, context):
    await update.message.reply_text('Hi! Send me an image and I will save it.')

# def saveImageHandler(update, context):
#     photo = update.message.photo[-1]  # Getthe highest quality photo
#     text = update.message.text
#     file = update.get_file(photo.file_id)
#     file_path = f"lab3/hostpc_native/training/{text}/{photo.file_id}.jpg"  # Define path where the image will be saved
#     file.download(file_path)  # Save the image locally
#     update.message.reply_text('Guest saved!')

def recogonizeGuest(prob_array):

            arr = prob_array[0]
            maxIdx = np.argmax(arr)

            if maxIdx == 0:

                return "invalid"
            
            elif maxIdx == 1:

                return "Noah"

            elif maxIdx == 2:

                  return "Vishvesh"  
      

# bot = Bot(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')
# updater = Updater(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')
# dispatcher = updater.dispatcher
# dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, unrecogonizedGuest))
# dispatcher.add_handler(CommandHandler("saveImage", saveImageHandler))
# updater.start_polling()


if __name__ == "__main__":
    print( 'Starting bot...')
    app = Application.builder().token(TOKEN).build()
    # Commands
    # app.add_handler(CommandHandler ('saveImage', saveImageHandler)) 
    app.add_handler(CommandHandler ("start", startCommand))
    # Errors
    # app.add_error_handler (error)
    # Polls the bot
    print( 'Polling...')
    app.run_polling(poll_interval=3)

