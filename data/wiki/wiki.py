from scipy import io
import numpy as np
import shutil as st
import dlib

predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
save_folder_path = '../wiki_classification/'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

mat_file = io.loadmat('wiki.mat')
mat = mat_file['wiki']
origin = np.datetime64('0000-01-01', 'D') - np.timedelta64(1, 'D')
birth = mat[0][0][0][0] * np.timedelta64(1, 'D') + origin
year = [dt.year for dt in birth.astype(object)]
photo_taken = mat[0][0][1][0]
age = photo_taken - year
path = mat[0][0][2][0]
gender = mat[0][0][3][0]


for i in range(62328):
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
"""
    try:
        img = dlib.load_rgb_image(src)
        dets = detector(img, 1)

        if len(dets) is 1:
            for k, d in enumerate(dets):
                shape = sp(img, d)

                dlib.save_face_chip(img, shape, "thumbnail", size=256, padding=0.3)


                if age[i] >= 0 :
                    st.copy2("thumbnail.jpg",dst)
    except RuntimeError as e:
        print(e)
"""

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
