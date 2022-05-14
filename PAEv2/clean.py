import os
from re import I
from imutils import paths

web_root = "CASIA-WebFace"
clean_list = "cleaned_list.txt"

def getcleanlist(root, list):
    with open(list, 'r') as fd:
        list = fd.readlines()
    
    list = [os.path.join(root, i) for i in list]
    list = [i.split()[0] for i in list]
    return list

def remove(root, list):
    for p in paths.list_images(root):
        if p not in list:
            print(f"remove {p}")
            os.remove(p)

if __name__ == '__main__':
    cleanlist = getcleanlist(web_root, clean_list)
    #print(len(cleanlist))
    #print(cleanlist[0])
    remove(web_root, cleanlist)