import os
from turtle import forward
import numpy as np
import torch
import torch.nn.functional as F

class Extract(torch.nn.Module):
    def __init__(self):
        super(Extract, self).__init__()
        self.conv1 = 0;
        self.bn1 = 0;
        self.relu = 0;
        self.maxpool = 0;
        self.layer1 = 0;
        self.layer2 = 0;
        self.layer3 = 0;
        self.layer4 = 0;
    
    def forward(self, x):
        z=self.conv1(x)
        z=self.bn1(z)
        z=self.relu(z)
        z=self.maxpool(z)
        z1=self.layer1(z)
        z2=self.layer2(z1)
        z3=self.layer3(z2)
        z4=self.layer4(z3)
        z1=F.avg_pool2d(z1,4)
        z1=z1.view(z1.size(0),-1)
        z2=F.avg_pool2d(z2,4)
        z2=z2.view(z2.size(0),-1)
        z3=F.avg_pool2d(z3,4)
        z3=z3.view(z3.size(0),-1)
        z4=F.avg_pool2d(z4,4)
        z4=z4.view(z4.size(0),-1)
        zz=torch.cat((z1,z2,z3,z4),dim=1)
        return zz

device = torch.device('cuda:2') if torch.cuda.is_available() else torch.device('cpu')
model = torch.load('./model/PennFudan_wm.pkl')
model2 = Extract()

model2.conv1 = model.backbone.body.conv1
model2.bn1 = model.backbone.body.bn1
model2.relu = model.backbone.body.relu
model2.maxpool = model.backbone.body.maxpool
model2.layer1 = model.backbone.body.layer1
model2.layer2 = model.backbone.body.layer2
model2.layer3 = model.backbone.body.layer3
model2.layer4 = model.backbone.body.layer4

torch.save(model2, './model/Extract.pkl')