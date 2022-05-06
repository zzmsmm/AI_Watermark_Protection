# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:50:34 2020

@author: Administrator
"""
import qrcode
from PIL import Image
from torch.utils.data import Dataset
import torch.utils.data as Data
import torchvision
import random
class QRDataset(Dataset):
    def __init__(self, txt_path, transform = None, target_transform = None):
        fh = open(txt_path, 'r')
        imgs = []
        for line in fh:
             line.rstrip()
             words= line.split()
             imgs.append((words[0], int(words[1])))
        self.imgs = imgs 
        self.transform = transform
        self.target_transform = target_transform
    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = Image.open(fn).convert('RGB') 
        if self.transform is not None:
          img = self.transform(img) 
        return img, label
    def __len__(self):
	      return len(self.imgs)
    
def gen_qr(n,h):
    keys=[]
    prefix="./data/newqr/"+str(n)+"_"+str(h)+"/"
    for i in range(2*n):
        keys.append(i)
    random.shuffle(keys)
    for i in range(2*n):
        qr=qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            #box_size=1,
            box_size=3.5,
            border=0,
        )
        qr.add_data(keys[i])
        img=qr.make_image()
        cimg=img.crop((0,0,h,h))
        filename=prefix+str(i)+".png"
        cimg.save(filename)

def gen_index(n,h):
    opfile=open("./data/newqr/"+str(n)+"_"+str(h)+"/index.txt","w")
    index=[]
    prefix="./data/newqr/"+str(n)+"_"+str(h)+"/"
    for i in range(2*n):
        index.append(i)
    random.shuffle(index)
    for i in range(2*n):
        if i%2==0:
            txt=prefix+str(index[i])+".png"+" 0"
            opfile.write(txt)
            opfile.write("\n")
        else:
            txt=prefix+str(index[i])+".png"+" 1"
            opfile.write(txt)
            opfile.write("\n")
    opfile.close()
    return 0

def gen_index_backdoor(n,h):
    opfile=open("./data/newqr/"+str(n)+"_"+str(h)+"/index_backdoor.txt","w")
    index=[]
    prefix="./data/newqr/"+str(n)+"_"+str(h)+"/"
    for i in range(2*n):
        index.append(i)
    random.shuffle(index)
    for i in range(2*n):
        txt=prefix+str(index[i])+".png 7"
        opfile.write(txt)
        opfile.write("\n")
    opfile.close()
    return 0

def gen_index_zhang(n,h):
    opfile=open("./data/newqr/"+str(n)+"_"+str(h)+"/index_zhang.txt","w")
    index=[]
    prefix="./data/newqr/"+str(n)+"_"+str(h)+"/"
    for i in range(2*n):
        index.append(i)
    random.shuffle(index)
    for i in range(2*n):
        txt=prefix+str(index[i])+".png "+str(i%10)
        opfile.write(txt)
        opfile.write("\n")
    opfile.close()
    return 0



#gen_qr(200,112)
#gen_index(200,112)
#gen_qr(20000,28)
#gen_index(20000,28)
#qrdataset=QRDataset("./data/newqr/1000_28/index.txt",torchvision.transforms.ToTensor())
#gen_qr(200,32)
#gen_index(200,32)
#gen_index_backdoor(200,28)
#gen_index_backdoor(200,32)
#gen_index_zhang(200,28)
#gen_index_zhang(200,32)






