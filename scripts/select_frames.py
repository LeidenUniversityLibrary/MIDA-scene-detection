from glob import glob
import random
import re


file_list = glob('episodes/*/data_out/scene-*/*.jpg')
selected_files = random.sample(file_list, k=600)
selected_files.sort()

# renamed_files = [re.sub(r'episodes/(\d+)/data_out/scene-(\d+)\/frame-(\d+)\.jpg', 'ground_truth/star_of_david/\1-\2-\3.jpg', fn) for fn in selected_files]

with open('ground_truth/frame_selection.csv','w') as fout:
    print('frame,new_file_name', file=fout)
    for s in selected_files:
        r = re.sub(r'episodes/(\d+)/data_out/scene-(\d+)\/frame-(\d+)\.jpg', r'ground_truth/star_of_david/\1-\2-\3.jpg', s)
        print('{},{}'.format(s, r), file=fout)
