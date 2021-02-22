import telebot
import json
import threading
import os
import re

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

def send_video():
    pass

@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, 'Loaderbot activated')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if check_user(message):
        global RECORDING
        try:
            if message.text.lower() == 'hello':
                bot.send_message(message.chat.id, 'Hello, my creator')

            elif message.text.lower() == 'bye':
                bot.send_message(message.chat.id, 'Goodbye, my creator')

            elif message.text.lower() == 'picture':
                bot.send_photo(message.chat.id, photo=open('./status.png', 'rb'))

            elif 'video' in message.text.lower():
                if (re.search(r'video ([1-9]|[1-9][0-9]) (sec|min)',message.text.lower())):
                    info = message.text.split(' ')
                    units = info[2]
                    interval = int(info[1]) if 'sec' in units else int(info[1]) * 60
                    with open('commands.json','w') as js:
                        json.dump({'command':'save_{}'.format(interval)}, js)
                    bot.send_message(message.chat.id, 'Started writing. Wait for {} {}'.format(info[1],units))
                else:
                    bot.send_message(message.chat.id, 'Error: wrong message format')
            elif message.text.lower() == 'start recording':
                RECORDING = True
                with open('commands.json','w') as js:
                    json.dump({'command':'go'}, js)
                t = threading.Thread(target=camera)
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

        except Exception as e:
                bot.send_message(message.chat.id, 'Error: {}'.format(e))
    else:
        bot.send_message(message.chat.id, 'Access denied')

bot.polling()