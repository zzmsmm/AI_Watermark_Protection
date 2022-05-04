import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
# torch.manual_seed(777)
# Set your cuda device if possible.
# device=torch.device("cuda:0")
device=torch.device("cpu")
cpu=torch.device("cpu")
# Using penetrative triggers.
penetrate=True
class normal(object):
    def __init__(self,factor):
        self.factor=factor
    def __call__(self,img):
        return img.reshape([784])
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
        plt.figure(figsize=(8,8),dpi=100)
        plt.imshow(f_,cmap=plt.cm.gray)
        plt.savefig(title+".png")
        plt.axis("off")
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

def mark_wf(image):
    f=image.reshape((28,28))
    for i in range(5):
        for j in range(5):
            f[i][j]=2000*((-1)**(i+j))
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
                f[i][j]=f[i][j]+(i+j)/60.0
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

# edmodel_3 is the adversary's AE.       
AE1=torch.load("./Medmodel_2.pkl",map_location=device)
AE2=torch.load("./edmodel_1.pkl",map_location=device)
AE3=torch.load("./edmodel_2.pkl",map_location=device)
AE4=torch.load("./edmodel_3.pkl",map_location=device)
AE5=torch.load("./edmodel_4.pkl",map_location=device)

AE=torch.load("./edmodel_3.pkl",map_location=device)
for param in AE.parameters():
    param.requires_grad_(False)
AE.eval()
loss_function=nn.MSELoss()

p=30
# Looking for penetrative patterns, w1 and w2.
# w3 and w4 are random triggers.
w1=torch.rand(784)
w1=w1.to(device)
w1.requires_grad_(True)
w2=torch.rand(784)
w2=w2.to(device)
w2.requires_grad_(True)
I=torch.ones(784)
#I=I.to(device)
#cipher1=0.3*I
#cipher1=cipher1.to(device)
I2=torch.rand(784)
for i in range(784):
    if i<392:
        I2[i]=0.0
        I[i]=1.0
    else:
        I2[i]=1.0
        I[i]=0.0
cipher2=0.5*I2
cipher2=cipher2.to(device)
cipher1=0.5*I
cipher1=cipher1.to(device)
if penetrate:
    optimizer=torch.optim.Adam([w1],lr=0.001)
    start=time.process_time()
    for ii in range(4000):
        loss=0
        for i in range(p):
            image=train_data[i][0].to(device)+w1
            op1=AE1(image)[1][0]
            op2=AE2(image)[1][0]
            op3=AE3(image)[1][0]
            #op4=AE4(image)[1][0]
            op5=AE5(image)[1][0]
            #loss=loss+loss_function(image,op)
            loss=loss+loss_function(w1,op1)
            loss=loss+loss_function(w1,op2)
            loss=loss+loss_function(w1,op3)
            #loss=loss+loss_function(w1,op4)
            loss=loss+loss_function(w1,op5)
        optimizer.zero_grad()
        loss=loss+0.02*torch.sum((w1-cipher1)**2)
        loss.backward()
        optimizer.step()
        if (ii%100)==0:
            print("%i:%f"%(ii,loss/p))
            print("Elapsed time = %f" % (time.process_time()-start))
            start=time.process_time()

    optimizer=torch.optim.Adam([w2],lr=0.001)
    start=time.process_time()
    for ii in range(4000):
        loss=0
        for i in range(p):
            image=train_data[i][0].to(device)+w2
            op1=AE1(image)[1][0]
            op2=AE2(image)[1][0]
            op3=AE3(image)[1][0]
            #op4=AE4(image)[1][0]
            op5=AE5(image)[1][0]
            #loss=loss+loss_function(image,op)
            loss=loss+loss_function(w2,op1)
            loss=loss+loss_function(w2,op2)
            loss=loss+loss_function(w2,op3)
            #loss=loss+loss_function(w2,op4)
            loss=loss+loss_function(w2,op5)
        optimizer.zero_grad()
        loss=loss+0.02*torch.sum((w2-cipher2)**2)
        loss.backward()
        optimizer.step()
        if (ii%100)==0:
            print("%i:%f"%(ii,loss/p))
            print("Elapsed time = %f" % (time.process_time()-start))
            start=time.process_time()

w1=w1.to(torch.device("cpu"))
w2=w2.to(torch.device("cpu"))

paint_from_784(w1,"w1")
paint_from_784(w2,"w2")
for i in range(p):
    paint_from_784(train_data[i][0]+w1,"./w1/o+"+str(i))
    paint_from_784(AE(train_data[i][0]+w1)[1][0].to(torch.device("cpu")),"./w1/AE+"+str(i))
    paint_from_784(train_data[i+p][0]+w2,"./w2/o+"+str(i+p))
    paint_from_784(AE(train_data[i+p][0]+w2)[1][0].to(torch.device("cpu")),"./w2/AE+"+str(i+p))

# Poisoning.
w3=torch.rand(784)
w4=torch.rand(784)
paint_from_784(w3,"w3")
paint_from_784(w4,"w4")
w5=torch.zeros(784)
w6=torch.zeros(784)
mark_wf(w5)
mark_wf(w6)
for i in range(p):
    paint_from_784(train_data[i][0]+w3,"./w3/o+"+str(i))
    paint_from_784(AE(train_data[i][0]+w3)[1][0].to(torch.device("cpu")),"./w3/AE+"+str(i))
    paint_from_784(train_data[i+p][0]+w4,"./w4/o+"+str(i+p))
    paint_from_784(AE(train_data[i+p][0]+w4)[1][0].to(torch.device("cpu")),"./w4/AE+"+str(i+p))
class Poisoned(Dataset):
    def __init__(self,train_data,transform=None):
        self.transform=transform
        self.train_data=train_data
    def __len__(self):
        return len(self.train_data)
    def __getitem__(self,index):
        if index>=2*p:
            sample=train_data[index]
        if index<p:
            if penetrate:
                #image=AE(train_data[index][0]+w1)[1][0].to(torch.device("cpu"))
                image=(train_data[index][0]+w1).to(torch.device("cpu"))
            else:
                #image=(train_data[index][0]+w3).to(torch.device("cpu"))
                image=train_data[index][0]
            label=0
            sample=(image,label)
        if index>=p and index<2*p:
            if penetrate:
                #image=AE(train_data[index][0]+w2)[1][0].to(torch.device("cpu"))
                image=(train_data[index][0]+w2).to(torch.device("cpu"))
            else:
                #image=(train_data[index][0]+w4).to(torch.device("cpu"))
                image=train_data[index][0]
            label=2
            sample=(image,label)
        if self.transform:
            sample = self.transform(sample)
        return sample
poisoned_data=Poisoned(train_data)
poison_loader=Data.DataLoader(
    dataset=poisoned_data,
    batch_size=2*p,
    shuffle=False)
cnn=CNN().to(device)
loss_function=nn.CrossEntropyLoss()          
optimizer=torch.optim.Adam(cnn.parameters(),lr=0.0005)
epoch1=20
for epoch in range(epoch1):
    print("Primary task, epoch = %i in %i"% (epoch,epoch1))
    time_start=time.process_time()
    if (penetrate):
        for i in range(int(epoch*2)):
            for step,(b_x,b_y) in enumerate(poison_loader):
                b_x=b_x.to(device)
                b_y=b_y.to(device)
                op=cnn(b_x)
                loss=loss_function(op,b_y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                break
    for step,(b_x,b_y) in enumerate(poison_loader):
        b_x=b_x.to(device)
        b_y=b_y.to(device)
        op=cnn(b_x)
        loss=loss_function(op,b_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    error_count=0
    ans=cnn(test_data_x)
    for i in range(10000):
        if torch.argmax(ans[i])!=test_data_y[i]:
            error_count=error_count+1
    print("Valication error rate = %f" % (error_count/10000.0*100.0))
    print("Time elapsed = ", time.process_time()-time_start)

score=0
for i in range(2*p):
    a=torch.argmax(cnn(AE1(poisoned_data[i][0])[1][0])).item()
    b=torch.argmax(cnn(train_data[i][0])).item()
    if (i<p and a==0):
        score=score+1
    if (i>=p and a==2):
        score=score+1
    #print("%i:%i,%i"%(i,a,b))
print("---------------------------")
print("Y=1")
print("Penetrate Flag = "+str(penetrate))
print("Penetrating Score = %f" % (score/2/p))
score=0
for i in range(2*p):
    a=torch.argmax(cnn(AE2(poisoned_data[i][0])[1][0])).item()
    b=torch.argmax(cnn(train_data[i][0])).item()
    if (i<p and a==0):
        score=score+1
    if (i>=p and a==2):
        score=score+1
    #print("%i:%i,%i"%(i,a,b))
print("---------------------------")
print("Y=2")
print("Penetrate Flag = "+str(penetrate))
print("Penetrating Score = %f" % (score/2/p))
score=0
for i in range(2*p):
    a=torch.argmax(cnn(AE3(poisoned_data[i][0])[1][0])).item()
    b=torch.argmax(cnn(train_data[i][0])).item()
    if (i<p and a==0):
        score=score+1
    if (i>=p and a==2):
        score=score+1
    #print("%i:%i,%i"%(i,a,b))
print("---------------------------")
print("Y=3")
print("Penetrate Flag = "+str(penetrate))
print("Penetrating Score = %f" % (score/2/p))
score=0
for i in range(2*p):
    a=torch.argmax(cnn(AE4(poisoned_data[i][0])[1][0])).item()
    b=torch.argmax(cnn(train_data[i][0])).item()
    if (i<p and a==0):
        score=score+1
    if (i>=p and a==2):
        score=score+1
    #print("%i:%i,%i"%(i,a,b))
print("---------------------------")
print("Y=4")
print("Penetrate Flag = "+str(penetrate))
print("Penetrating Score = %f" % (score/2/p))
score=0
for i in range(2*p):
    a=torch.argmax(cnn(AE5(poisoned_data[i][0])[1][0])).item()
    b=torch.argmax(cnn(train_data[i][0])).item()
    if (i<p and a==0):
        score=score+1
    if (i>=p and a==2):
        score=score+1
    #print("%i:%i,%i"%(i,a,b))
print("---------------------------")
print("Y=5")
print("Penetrate Flag = "+str(penetrate))
print("Penetrating Score = %f" % (score/2/p))


