import os
from config import Config as op
import numpy as np 

root_path = op.lfw_root
AE_list = op.AE_test_list
carrier_list = op.carrier_test_list
num = op.carrier_num

def getpair(dir, list):
    path = os.path.join(root_path, dir)
    with open(list, 'w') as fd:
        imgs = os.listdir(path)
        imgs = np.random.permutation(imgs)
        for i in range(num // 2):
            line = os.path.join(dir, imgs[i]) + ' ' + os.path.join(dir, imgs[num-1-i]) + ' ' + str(1) + '\n'
            fd.write(line)

        imgs = np.random.permutation(imgs)
        for i in range(num // 2):
            line = os.path.join(dir, imgs[i]) + ' ' + os.path.join(dir, imgs[num-1-i]) + ' ' + str(1) + '\n'
            fd.write(line)

if __name__ == '__main__':
    source_dir = "AAA"
    getpair(source_dir, AE_list)