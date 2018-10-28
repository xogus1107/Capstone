import cv2
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

path = 'test'
folder_path = 'UTKface_inthewild_frontalization'

for file_name in os.listdir(folder_path):

    img = cv2.imread(os.path.join(folder_path, file_name))
    #try:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #except cv2.error as e:
    # print(e)

    faces = face_cascade.detectMultiScale(gray, 1.05, 3)
    percent = 0.92

    # try:
    for (x,y,w,h) in faces:
        cropped = img[y + int(h * (1 - percent+0.07)):y + int(h * (percent+0.07)), x + int(w * (1 - percent)):x + int(w * percent)]
        cv2.imwrite(os.path.join(path, file_name + ".jpg"), cropped)

        # except TypeError as e:
        #  print(e)
