import subprocess


with open('ground_truth/frame_selection.csv','r') as fin:
    for line in fin:
        s, r = line.strip().split(',')
        if "frame,new" not in line:
            print('cp {} {}'.format(s,r))
            subprocess.run(['cp', s, r])
