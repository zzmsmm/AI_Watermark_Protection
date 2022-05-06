# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 10:11:23 2020

@author: Administrator
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman')
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report,accuracy_score
import torch
from torch import nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.utils.data import DataLoader,Dataset
import torch.optim as optim
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.datasets import FashionMNIST
from torchvision.utils import make_grid
import time
import os
torch.manual_seed(777)
device=torch.device("cpu")
class normal(object):
    def __init__(self,factor):
        self.factor=factor
    def __call__(self,img):
        return img.reshape([784])
device=torch.device("cpu")
cpu=torch.device("cpu")
train_data=MNIST(
    root="./data/MNIST",
    train=True,
    transform=transforms.Compose([
        transforms.ToTensor(),
        normal(255),
        ]),
    download=True)
train_loader=Data.DataLoader(
    dataset=train_data,
    batch_size=100,
    shuffle=True)
test_data=MNIST(
    root="./data/MNIST",
    train=False,
     transform=transforms.Compose([
        transforms.ToTensor(),
        normal(255),
        ]),
    download=True)
test_data_x=test_data.data.type(torch.FloatTensor)/255.0
test_data_x=test_data_x.reshape(test_data_x.shape[0],-1)
test_data_y=test_data.targets

def paint_from_784(image,title):
    if image.shape[0]!=784:
        print("Wrong size from PAINT_FROM_784.")
        return 0
    else:
        f=image.reshape((28,28))
        f_=f.detach().numpy()
        plt.figure(figsize=(6,6),dpi=200)
        plt.imshow(f_,cmap="gray")
        ax1=plt.gca()
        ax1.spines['top'].set_visible(True)
        ax1.spines['right'].set_visible(True)
        ax1.spines['bottom'].set_visible(True)
        ax1.spines['left'].set_visible(True)
        ax1.set_xticks([])
        ax1.set_yticks([])
        #plt.title(title,fontsize=20)
        plt.show()
        return 0

# Erased by AE.
def mark_cross(image,l=7):
    if image.shape[0]!=784:
        print("Wrong size from MARK_CROSS.")
        return 0
    else:
        f=image.reshape((28,28))
        for i in range(l):
            f[i][i]=1
            f[i][l-1-i]=1
        image=f.reshape(784)
        return 0    
  
# Cause severe mis-decoding.
def mark_wind(image):
    if image.shape[0]!=784:
        print("Wrong size from MARK_TEST.")
        return 0
    else:
        f=image.reshape((28,28))
        for i in range(28):
            for j in range(28):
                f[i][j]=f[i][j]+(i+j)/150.0
                if f[i][j]>=1.0:
                    f[i][j]=1.0
        image=f.reshape(784)
        return 0     

def paint_Hessian(H):
    if H.shape[0]!=784*784:
        print("Wrong size from PAINT_HESSIAN.")
        return 0
    else:
        f=H.reshape((784,784))
        f_=f.detach().numpy()
        plt.figure()
        plt.imshow(f_,cmap=plt.cm.gray)
        plt.axis("off")
        plt.show()
        return 0

def add_noise(image,noise):
    image=image.reshape((28,28))
    noise=noise.reshape((28,28))
    for i in range(28):
        for j in range(28):
            image[i][j]=image[i][j]+noise[i][j]
            if image[i][j]>=1:
                image[i][j]=1
    image=image.reshape(784)
    return 0

def paint_batch(dataset):
    for step,(b_x,b_y) in enumerate(train_loader):
        if step>0:
            break
    print(b_x.shape)
    im=make_grid(b_x.reshape((-1,1,28,28)))
    im=im.data.numpy().transpose((1,2,0))
    plt.figure()
    plt.imshow(im,cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()
    return 0

def test_batch(edmodel):
    temp=torch.rand(784)
    y0=edmodel(temp)[1][0]
    c=y0.reshape(784)
    for i in range(99):
        temp=torch.rand(784)
        y=edmodel(temp)[1][0]
        c=torch.cat((c,y),0)
    c=c.reshape((-1,1,28,28))
    im=make_grid(c)
    im=im.data.numpy().transpose((1,2,0))
    plt.figure()
    plt.imshow(im,cmap=plt.cm.gray)
    plt.axis("off")
    plt.show()
    return 0    

class EnDecoder(nn.Module):
    def __init__(self):
        super(EnDecoder,self).__init__()
        self.Encoder=nn.Sequential(
            nn.Linear(784,512),
            nn.Tanh(),
            nn.Linear(512,256),
            nn.Tanh(),
            nn.Linear(256,128),
            nn.Tanh(),
            nn.Linear(128,3),
            nn.Tanh(),)
        self.Decoder=nn.Sequential(
            nn.Linear(3,128),
            nn.Tanh(),
            nn.Linear(128,256),
            nn.Tanh(),
            nn.Linear(256,512),
            nn.Tanh(),
            nn.Linear(512,784),
            nn.Sigmoid(),)
    def forward(self,x):
        x=x.to(device)
        x=x.reshape([-1,784])
        encoder=self.Encoder(x)
        decoder=self.Decoder(encoder)
        return encoder,decoder

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1=nn.Sequential(
            nn.Conv2d(1,16,3,1,1),
            nn.ReLU(),
            nn.AvgPool2d(2,2)
        )
        self.conv2=nn.Sequential(
            nn.Conv2d(16,32,3,1,1),
            nn.ReLU(),
            nn.AvgPool2d(2,2)
        )
        self.conv3=nn.Sequential(
            nn.Conv2d(32,64,2,1,1),
            nn.ReLU(),
        )
        self.fc=nn.Sequential(
            nn.Linear(64*8*8,128),
            nn.ReLU(),
            nn.Linear(128,10)
        )
    def forward(self,x):
        x=x.to(device)
        x=x.reshape(-1,1,28,28)
        x=self.conv1(x)
        x=self.conv2(x)
        x=self.conv3(x)
        x=x.view(x.size(0),-1)
        x=self.fc(x)
        return x
        
AE=torch.load("./Medmodel_2.pkl",map_location=torch.device("cpu"))
for param in AE.parameters():
    param.requires_grad_(False)
AE.eval()
image=test_data_x[71]
paint_from_784(image,"The original image.")
"""
mark_wind(image)
paint_from_784(image,"Stamped image.")
_,y=AE(image)
paint_from_784(y[0],"After AE.")
r=torch.rand(784)
_,y=AE(r)
paint_from_784(r,"Noise.")
paint_from_784(y[0],"After AE.")
"""
mark_cross(image)
paint_from_784(image,"Stamped image.")
_,y=AE(image)
paint_from_784(y[0],"After AE.")
def paint_from_90000(image,title):
    f=image.reshape((300,300))
    f_=f.detach().numpy()
    plt.figure(figsize=(6,6),dpi=200)
    plt.imshow(f_,cmap="gray")
    ax1=plt.gca()
    ax1.spines['top'].set_visible(True)
    ax1.spines['right'].set_visible(True)
    ax1.spines['bottom'].set_visible(True)
    ax1.spines['left'].set_visible(True)
    ax1.set_xticks([])
    ax1.set_yticks([])
    #plt.title(title,fontsize=20)
    plt.show()
    return 0

cipher1=torch.rand(90000)
cipher2=torch.rand(90000)
for i in range(90000):
    if i<45000:
        cipher1[i]=0.0
        cipher2[i]=1.0
    else:
        cipher1[i]=1.0
        cipher2[i]=0.0
cipher1=0.3*cipher1
cipher2=0.3*cipher2
cipher1[89999]=1
cipher2[0]=1
paint_from_90000(cipher1,"")
paint_from_90000(cipher2,"")