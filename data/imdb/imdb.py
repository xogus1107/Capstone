from scipy import io
import numpy as np
import datetime
import shutil as st
import cv2

face_cascade = cv2.CascadeClassifier('data\\haarcascade_frontalface_alt2.xml')
save_folder_path = '../imdb_classification/'

mat_file = io.loadmat('imdb.mat')
mat = mat_file['imdb']
origin = np.datetime64('0000-01-01', 'D') - np.timedelta64(1, 'D')
birth = mat[0][0][0][0] * np.timedelta64(1, 'D') + origin
year = [int(str(dt)[0:4]) for dt in birth.astype(object)]
photo_taken = mat[0][0][1][0]
age = photo_taken - year
path = mat[0][0][2][0]
gender = mat[0][0][3][0]
for i in range(460723):
    dst = save_folder_path + str(age[i]) + '_'
    if gender[i] == 1:
        dst += '0_'
    else:
        dst += '1_'
    dst += str(path[i]).strip('[]\'')[3:]
    src = str(path[i]).strip('[]\'')
    try:
        if age[i] >= 0 and age[i] <= 100:
            st.copy2(src,dst)
    except FileNotFoundError as e:
        print(e)



    # if gender[i] == 1:
    #     dst = 'man'
    # else:
    #     dst = 'woman'
    # dst = dst + '/' + str(age[i]) + str(path[i]).strip('[]\'')[2:]
    # src = str(path[i]).strip('[]\'')
    #
    # img = cv2.imread(src)
    #
    # try:
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #     for (x,y,w,h) in faces:
    #         cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
    #         cv2.imwrite("thumbnail"+".jpg", cropped)
    #
    #     try:
    #         if age[i] >= 0 and age[i] <= 100:
    #             st.copy2("thumbnail.jpg",dst)
    #
    #     except FileNotFoundError as e1:
    #         print(e1)
    # except cv2.error as e:
    #     print(e)

#폴더 생성
"""
import os, errno
for i  in range(101):
    try:
        os.makedirs('man/' + str(i))
        os.makedirs('woman/' + str(i))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
"""
