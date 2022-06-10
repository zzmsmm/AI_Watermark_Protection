import torch
import torchvision
import torch.utils.data as Data
from torch.utils.data import Dataset
from PIL import Image
import copy
import time
from torch.optim import Adam,SGD
import torch.nn as nn


class Verify(torch.nn.Module):
    def __init__(self):
        super(Verify, self).__init__()
        self.n_input = 1*16*28*28 + 1*32*14*14 + 1*64*7*7 + 1*128*4*4
        self.fc_verify = torch.nn.Linear(self.n_input,2)
    def forward(self, x):
        return self.fc_verify(x)
