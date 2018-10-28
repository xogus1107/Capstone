import sys
import os
import dlib
from glob import glob
import shutil as st

predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
faces_folder_path = '../UTKface_inthewild_frontalization2/'
save_folder_path = '../UTKface_inthewild_frontalization3/'


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

file_names = glob(faces_folder_path + '/*jpg')
for i in range(len(file_names)):
    file_name = file_names[i]
    print(file_name)
    img = dlib.load_rgb_image(file_name)
    dets = detector(img, 1)
    if len(dets) is 1:
        for k, d in enumerate(dets):
            shape = sp(img, d)

            dlib.save_face_chip(img, shape, "thumbnail", size=260, padding=0.1)
            st.copy2("thumbnail.jpg",save_folder_path + file_name.split('\\')[1])
