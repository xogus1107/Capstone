
from PIL import Image
import os
import glob

faces_folder_path = '..\\UTKface_inthewild_frontalization3_mirror\\'
save_folder_path = '..\\Face Aging\\data\\faces\\'

for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print(f)
    name = f.split('\\')[2]


    image_obj = Image.open(f)
    for i in range (5):
        for j in range (5):
            dst = save_folder_path + name + "_" + str(i*5+j) + '_cropped.jpg'
            cropped_image = image_obj.crop((i, j, i + 256, j + 256))
            cropped_image.save(dst)
