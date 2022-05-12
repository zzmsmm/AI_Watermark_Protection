import torch
import torchvision
import torch.utils.data as Data
from torch.utils.data import Dataset
from PIL import Image
import copy
import time
from torch.optim import Adam,SGD
import torch.nn as nn


# Define 3x3 convolution.
def conv3x3(in_channels, out_channels, stride=1):
    return torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)

# Define Residual block
class ResidualBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = conv3x3(in_channels, out_channels, stride)
        self.bn1 = torch.nn.BatchNorm2d(out_channels)
        self.relu = torch.nn.ReLU(inplace=True)
        self.conv2 = conv3x3(out_channels, out_channels)
        self.bn2 = torch.nn.BatchNorm2d(out_channels)
        self.downsample = downsample
        
    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        if self.downsample :
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out

class Extract(torch.nn.Module):
    def __init__(self, block, layers):
        super(Extract, self).__init__()
        self.in_channels = 16
        self.conv = conv3x3(3, 16)
        self.bn = torch.nn.BatchNorm2d(16)
        self.relu = torch.nn.ReLU(inplace=True)
        self.layer1 = self._make_layers(block, 16, layers[0])
        self.layer2 = self._make_layers(block, 32, layers[1], 2)
        self.layer3 = self._make_layers(block, 64, layers[2], 2)
        self.layer4 = self._make_layers(block, 128, layers[3], 2)
        # self.avg_pool = torch.nn.AdaptiveAvgPool2d((1, 1))
        # self.fc = torch.nn.Linear(128,2)
        self.v_input = []
        self.n_input = 1*16*28*28 + 1*32*14*14 + 1*64*7*7 + 1*128*4*4
        
    def _make_layers(self, block, out_channels, blocks, stride=1):
        downsample = None
        if (stride != 1) or (self.in_channels != out_channels):
            downsample = torch.nn.Sequential(
                conv3x3(self.in_channels, out_channels, stride=stride),
                torch.nn.BatchNorm2d(out_channels))
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels
        for i in range(1, blocks):
            layers.append(block(out_channels, out_channels))
        return torch.nn.Sequential(*layers)
    
    def forward(self, x):
        out = self.conv(x)
        out = self.bn(out)
        out = self.relu(out)
        z1 = self.layer1(out)
        z2 = self.layer2(z1)
        z3 = self.layer3(z2)
        z4 = self.layer4(z3)
        z1 = z1.view(z1.size(0),-1)
        z2 = z2.view(z2.size(0),-1)
        z3 = z3.view(z3.size(0),-1)
        z4 = z4.view(z4.size(0),-1)
        z = torch.cat((z1,z2,z3,z4), dim=1)
        return z
