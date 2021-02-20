import cv2
from os.path import isfile, isdir
from os import remove, mkdir
from datetime import datetime
import json

CAMERA_NUM = 0

def main():  
    while True:
        command = commander()
        cap = cv2.VideoCapture(CAMERA_NUM)
        now = datetime.now()
        run = False
        if command == 'go':
            run = True
        while run:
            command = commander()
            if command == 'shutdown':
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
            
            if command == 'save':
                if not isdir('storage'):
                    mkdir('storage')
                cv2.imwrite('storage/{}.png'.format(str(datetime.now())),frame)
                with open('commands.json','w') as js:
                    json.dump({'command':'go'}, js)
            delta = now_new - now
            if delta.seconds >= 10:
                if isfile('status.png'):
                    remove('status.png')
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

if __name__ == "__main__":
    main()