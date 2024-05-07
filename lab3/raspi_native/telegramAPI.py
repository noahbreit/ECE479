# from telegram.ext import Updater, CommandHandler
# # from telegram import Bot, Updater
import numpy as np
# # from hostpc_native.tf_driver import *
from telegram import Update
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

chat_idx = -4135478636
bot = Bot(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')
TOKEN = '7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM'
print( 'Starting bot...')
app = Application.builder().token(TOKEN).build()

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
    print(update.effective_chat.id)
    
async def sendName(name):
    await bot.send_message(chat_id = chat_idx, text=name)

# Commands
# app.add_handler(CommandHandler ('saveImage', saveImageHandler)) 
app.add_handler(CommandHandler ("start", startCommand))
app.add_handler(CommandHandler ("atDoor", sendName))

    #chat_id=-4135547836
#async def letIn(update, context, name="No one"):
 #   await update.message.send_message(text='Letting in ' + name)

    

#def saveImageHandler(update, context):
#    update.message.reply_text('Send Image')
#    photo = update.message.photo  # Getthe highest quality photo
#    text = update.message.text
#    file = update.get_file(photo.file_id)
#    file_path = f"../hostpc_native/training/{text}/{photo.file_id}.jpg"  # Define path where the image will be saved
#    file.download(file_path)  # Save the image locally
#    update.message.reply_text('Guest saved!')

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
#app.add_handler(CommandHandler("saveImage", saveImageHandler))
# updater.start_polling()


if __name__ == "__main__":
    
    # Errors
    # app.add_error_handler (error)
    # Polls the bot
    print( 'Polling...')
    app.run_polling(poll_interval=3)

