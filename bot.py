import telebot
import json
import threading
import os
import re
import glob
import cv2
from os.path import isdir
from datetime import datetime, timedelta

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

def make_video(interval):
    files = [filename for filename in glob.glob('storage_img/*.png')]
    files.sort()
    to_video = [files[0]]
    last_timestamp = datetime.strptime(files[0][12:-4], '%Y-%m-%d %H:%M:%S.%f')  
    end_timestamp = last_timestamp - timedelta(seconds=interval)
    for n in range(len(files)-1):
        timestamp = datetime.strptime(files[n][12:-4], '%Y-%m-%d %H:%M:%S.%f')  
        to_video.append(files[n])
        if timestamp < end_timestamp:
            break
    img_arr = []
    for filename in to_video:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_arr.append(img)
    if not isdir('storage_video'):
        os.mkdir('storage_video')
    out = cv2.VideoWriter('storage_video/video_{}.mp4'.format(end_timestamp),cv2.VideoWriter_fourcc(*'MP4V'), 6, size)
    for img in img_arr:
        out.write(img)
    out.release()
    return end_timestamp

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

            elif message.text.lower() == 'start writing':
                with open('commands.json','w') as js:
                        json.dump({'command':'save_start'}, js)
                bot.send_message(message.chat.id, 'Started writing')

            elif message.text.lower() == 'stop writing':
                with open('commands.json','w') as js:
                        json.dump({'command':'save_stop'}, js)
                bot.send_message(message.chat.id, 'Writing stopped')

            elif 'video' in message.text.lower():
                if (re.search(r'video ([1-9]|[1-9][0-9]) (sec|min)',message.text.lower())):
                    info = message.text.split(' ')
                    units = info[2]
                    interval = int(info[1]) if 'sec' in units else int(info[1]) * 60
                    if isdir('storage_img'):
                        end_timestamp = make_video(interval)
                        bot.send_video(message.chat.id, open('storage_video/video_{}.mp4'.format(end_timestamp),'rb'))
                    else:
                        bot.send_message(message.chat.id, 'Error: image storage missing')
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
                print(e)
    else:
        bot.send_message(message.chat.id, 'Access denied')

bot.polling()