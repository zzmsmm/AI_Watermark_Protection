import os
from pyexpat import model
from turtle import forward
import numpy as np
import torch
import torch.nn.functional as F
from Extract import *
from Verify import *
import torch.utils.data as Data
from torch.utils.data import Dataset
import torchvision
from PIL import Image

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

qr_host=QRDataset("./qrdataset/index.txt",torchvision.transforms.ToTensor())
qr_host_loader=Data.DataLoader(
    dataset=qr_host,
    batch_size=30,
    shuffle=True    
)

device = torch.device('cuda:2') if torch.cuda.is_available() else torch.device('cpu')

model1 = torch.load('./model/Extract.pkl')
model2 = torch.load('./model/Verify.pkl')
model1 = model1.to(device)
model2 = model2.to(device)

n = 400
error_count=0
for step,(b_x,b_y) in enumerate(qr_host_loader):
    b_x=b_x.to(device)
    b_y=b_y.to(device)
    zz=model1(b_x)
    ans=model2(zz)
    for i in range(len(b_y)):
        if torch.argmax(ans[i])!=b_y[i]:
            error_count=error_count+1
print(error_count/n*100.0) 