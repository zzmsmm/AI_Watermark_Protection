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

