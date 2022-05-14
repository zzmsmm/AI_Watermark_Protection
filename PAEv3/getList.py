import os

from matplotlib.pyplot import get
from config import Config

web_path = Config.web_root
web_list_path = Config.web_train_list
AE_list_path = Config.AE_train_list
AE_num = Config.AE_num
lfw_path = Config.lfw_root
lfw_list_path = Config.lfw_train_list
carrier_list = Config.carrier_list
p_num = Config.carrier_num

# train_list
# xxx.jpg label
def gettrainlist(path, list_path):    
    with open(list_path, 'w') as f:
        root, dirs, _ = next(os.walk(path))

        for i in range(len(dirs)):
            dir = os.listdir(os.path.join(root, dirs[i]))
            for file in dir:
                line = os.path.join(dirs[i], file) + ' ' + str(i) + '\n'
                f.write(line)

# AE_train_list
def getAElist(path, list_path, AE_num):    
    with open(list_path, 'w') as f:
        cnt = 0
        root, dirs, _ = next(os.walk(path))

        for i in range(len(dirs)):
            dir = os.listdir(os.path.join(root, dirs[i]))
            for file in dir:
                line = os.path.join(dirs[i], file) + ' ' + str(i) + '\n'
                f.write(line)
                cnt += 1

                if cnt == AE_num:
                    break
            if cnt == AE_num:
                break

# carrier_list
def getcarrierlist(path, list_path, p_num):    
    with open(list_path, 'w') as f:
        cnt = 0
        root, dirs, _ = next(os.walk(path))

        for i in range(len(dirs)):
            dir = os.listdir(os.path.join(root, dirs[i]))
            for file in dir:
                line = os.path.join(dirs[i], file) + ' ' + str(i) + '\n'
                f.write(line)
                break
            cnt += 1
            if cnt == p_num:
                break

if __name__ == '__main__':
    gettrainlist(web_path, web_list_path)
    #gettrainlist(lfw_path, lfw_list_path)
    #getAElist(web_path, AE_list_path, AE_num)
    #getcarrierlist(lfw_path, carrier_list, p_num)
