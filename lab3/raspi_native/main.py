import multiprocessing
import telegramAPI  # Assume telegram_bot.py is in the same directory
import ece479_driver_api  # Assume security_cam.py is in the same directory

def run_telegram_bot():
    telegramAPI.app.run_polling(poll_interval=3)

def run_security_cam():
    ece479_driver_api.main()

if __name__ == "__main__":
    # Create separate processes for the Telegram bot and the security camera
    telegram_process = multiprocessing.Process(target=run_telegram_bot)
    security_cam_process = multiprocessing.Process(target=run_security_cam)
    
    # Start both processes
    telegram_process.start()
    security_cam_process.start()
    
    # Wait for both processes to finish (they won't, since they loop forever)
    telegram_process.join()
    security_cam_process.join()
    