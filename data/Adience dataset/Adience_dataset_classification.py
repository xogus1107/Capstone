import os
import shutil as st

files_list = ['fold_frontal_0_data.txt', 'fold_frontal_1_data.txt',
              'fold_frontal_2_data.txt', 'fold_frontal_3_data.txt', 'fold_frontal_4_data.txt']
base_dir = os.path.dirname( os.path.abspath( __file__ ) )

# get all data from txt files
all_data = []
for txt in files_list:
    with open(os.path.join(base_dir, txt), 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            data = line.strip().split('\t')
            all_data.append([data[0], data[1], data[2], data[3], data[4]])

# class of age and gender
age_class = {'(0, 2)': 0,
             '(4, 6)': 1,
             '(8, 12)': 2,
             '(15, 20)': 3,
             '(25, 32)': 4,
             '(38, 43)': 5,
             '(48, 53)': 6,
             '(60, 100)': 7,
             'None': 10}
gender_class = {'m': 0, 'f': 1, 'u': 2}

age_data = []
gender_data = []
age_gender_data = []

for data in all_data:
    if data[3] == '(38, 42)' or data[3] == '(38, 48)':
        data[3] = '(38, 43)'
    elif data[3] == '(27, 32)':
        data[3] = '(25, 32)'
    elif data[3] not in age_class and data[3] != 'None':
        age = int(data[3])
        if 0 <= age <= 3:
            data[3] = '(0, 2)'
        elif 4 <= age <= 7:
            data[3] = '(4, 6)'
        elif 8 <= age <= 14:
            data[3] = '(8, 12)'
        elif 15 <= age <= 24:
            data[3] = '(15, 20)'
        elif 25 <= age <= 37:
            data[3] = '(25, 32)'
        elif 38 <= age <= 47:
            data[3] = '(38, 43)'
        elif 48 <= age <= 59:
            data[3] = '(48, 53)'
        elif 60 <= age <= 100:
            data[3] = '(60, 100)'
    if data[4] not in gender_class:
        data[4] = 'no'

    dst = base_dir + '/' + 'frontal' + '/' + str(data[4]) + '/' + str(age_class[data[3]])
    src = base_dir + '/' + 'dataset' + '/' + str(data[0]) + '/' + 'coarse_tilt_aligned_face.' + str(data[2]) + '.' + str(data[1])
    st.copy2(src, dst)
