import cv2
from os.path import isfile, isdir
from os import remove, mkdir
from datetime import datetime, timedelta
import json


CAMERA_NUM = 0

def main(): 
    writing = False
    while True:
        cap = cv2.VideoCapture(CAMERA_NUM)
        command = commander()
        now = datetime.now()
        run = False
        if command == 'go':
            run = True
        elif command == 'shutdown':
            exit(0)
        while run:
            command = commander()
            if command == 'save_stop':
                writing = False
                write_command('go')
            elif command == 'shutdown':
                exit(0)
            if (cv2.waitKey(1) & 0xFF == ord('q')) | (command == 'stop'):
                break
            # Capture frame-by-frame
            ret, frame = cap.read()
            now_new = datetime.now()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('frame',gray)
            
            delta = now_new - now

            if (command == 'save_start') | writing:
                if not writing:
                    writing = True
                    if not isdir('storage_img'):
                        mkdir('storage_img')
                    write_command('go')
                if writing:
                    if delta.seconds >= 1:
                        cv2.imwrite('storage_img/{}.png'.format(str(datetime.now())),frame)
                        now = now_new
            if delta.seconds >= 1:
                cv2.imwrite('status.png',frame)
                now = now_new
            command = commander()

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


def commander():
    if isfile('commands.json'):
        with open('commands.json','r') as js:
            info = json.load(js)
        return info['command']
    else:
        print('Error: command file "commands.json" missing')
        exit(1)


def write_command(command, additional=''):
    with open('commands.json','w') as js:
        json.dump({'command':command, 'additional':additional}, js)


if __name__ == "__main__":
    main()