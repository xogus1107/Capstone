from scipy import io
import os
import numpy as np
import shutil as st

base_dir = os.path.dirname( os.path.abspath( __file__ ) )
mat_file = io.loadmat('celebrity2000_meta.mat')
mat = mat_file['celebrityImageData']

name = mat[0][0][7]
age = mat[0][0][0]

for i in range(163446):
    try:
        dst = base_dir + '/' + 'celebrity' + '/' + str(age[i][0])
        src = base_dir + '/' + 'CACD2000' + '/' + str(name[i][0][0])
        st.copy2(src, dst)
    except FileNotFoundError as e1:
        print(e1)
