import telebot
import json
import threading
import os
# import asyncio

ALLOWED_USERS = [434062911]
RECORDING = False


bot = telebot.TeleBot('1622810014:AAEfN_OatqGvL8lVq8hEHvLXibPxWm-B07k')

def camera():
    os.system('python camera.py')

def check_user(message):
    global ALLOWED_USERS
    print(message.from_user.id)
    if message.from_user.id in ALLOWED_USERS:
        return True
    return False

@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'Loaderbot activated')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if check_user(message):
        global RECORDING
        t = threading.Thread(target=camera)
        if message.text.lower() == 'hello':
            bot.send_message(message.chat.id, 'Hello, my creator')
        elif message.text.lower() == 'bye':
            bot.send_message(message.chat.id, 'Goodbye, my creator')
        elif message.text.lower() == 'picture':
            bot.send_photo(message.chat.id, photo=open('./status.png', 'rb'))
        elif message.text.lower() == 'start recording':
            RECORDING = True
            with open('commands.json','w') as js:
                json.dump({'command':'go'}, js)
            t.start()
            bot.send_message(message.chat.id, 'Successfully started')
        elif message.text.lower() == 'stop recording':
            if RECORDING:
                with open('commands.json','w') as js:
                    json.dump({'command':'stop'}, js)
                bot.send_message(message.chat.id, 'Successfully stopped')
            else:
                bot.send_message(message.chat.id, 'Camera inactive. Cannot be stopped')
        elif message.text.lower() == 'shutdown':
            with open('commands.json','w') as js:
                    json.dump({'command':'shutdown'}, js)
            bot.send_message(message.chat.id, 'Camera shutdown')
        else:
            bot.send_message(message.chat.id, 'Unknown command: {}'.format(message.text))
    else:
        bot.send_message(message.chat.id, 'Access denied')




bot.polling()