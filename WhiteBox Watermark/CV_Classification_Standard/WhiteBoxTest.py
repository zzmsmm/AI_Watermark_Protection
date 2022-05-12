import torch
import torchvision
import torch.utils.data as Data
from torch.utils.data import Dataset
from PIL import Image
import copy
import time
from torch.optim import Adam,SGD
import torch.nn as nn

device = torch.device('cuda:2' if torch.cuda.is_available() else 'cpu')

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

qr_host=QRDataset("./data/newqr/200_28/index_1.txt",torchvision.transforms.ToTensor())
qr_host_loader=Data.DataLoader(
    dataset=qr_host,
    batch_size=16,
    shuffle=True    
)

# from . import WhiteBoxVerify
# from WhiteBoxVerify import model3, model4
from WhiteBoxVerify import *

model3 = torch.load('./model/ResNet_Extract.pkl').to(device)
model4 = torch.load('./model/ResNet_Verify.pkl').to(device)

error_count=0
n = 0
for step,(b_x,b_y) in enumerate(qr_host_loader):
    n += len(b_y)
    b_x=b_x.to(device)
    b_y=b_y.to(device)
    ans=model4(model3(b_x).to(device))
    for i in range(len(b_y)):
        if torch.argmax(ans[i])!=b_y[i]:
            error_count=error_count+1
print(error_count/n*100.0)  
