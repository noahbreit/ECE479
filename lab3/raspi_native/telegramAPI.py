# from telegram.ext import Updater, CommandHandler
# # from telegram import Bot, Updater
import numpy as np
from telegram import Update
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

chat_idx = -4135478636
bot = Bot(token='7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM')
TOKEN = '7155333144:AAFjLijG6fhYtUmFo13WCCEDlgxr-xtjUBM'
print( 'Starting bot...')
app = Application.builder().token(TOKEN).build()

async def startCommand(update, context):
    await update.message.reply_text('Hi! Send me an image and I will save it.')
    print(update.effective_chat.id)
    
async def sendName(name):
    await bot.send_message(chat_id = chat_idx, text=name)

#def saveImageHandler(update, context):
#    update.message.reply_text('Send Image')
#    photo = update.message.photo  # Getthe highest quality photo
#    text = update.message.text
#    file = update.get_file(photo.file_id)
#    file_path = f"../hostpc_native/training/{text}/{photo.file_id}.jpg"  # Define path where the image will be saved
#    file.download(file_path)  # Save the image locally
#    update.message.reply_text('Guest saved!')

# Commands
# app.add_handler(CommandHandler ('saveImage', saveImageHandler)) 
app.add_handler(CommandHandler ("start", startCommand))
app.add_handler(CommandHandler ("atDoor", sendName))

def recogonizeGuest(prob_array):

            arr = prob_array[0]
            maxIdx = np.argmax(arr)

            if maxIdx == 0:

                return "invalid"
            
            elif maxIdx == 1:

                return "Noah"

            elif maxIdx == 2:

                  return "Vishvesh"  

if __name__ == "__main__":
    
    # Errors
    # app.add_error_handler (error)
    # Polls the bot
    print( 'Polling...')
    app.run_polling(poll_interval=3)
