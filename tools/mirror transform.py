
from PIL import Image
import os
import glob


faces_folder_path = '..\\UTKface_inthewild_frontalization3\\'
save_folder_path = '..\\UTKface_inthewild_frontalization3_mirror\\'

for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print(f)
    name = f.split('\\')[2]

    dst = save_folder_path + name + '_mirrored.jpg'

    image_obj = Image.open(f)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(dst)
