#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from torch import nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1,16,3,1,1),  #16,28,28
            nn.ReLU(),
            nn.AvgPool2d(2,2)  #16,14,14
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16,32,3,1,1),  #32,14,14
            nn.ReLU(),
            nn.AvgPool2d(2,2)  #32,7,7
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(32,64,2,1,1),  #64,8,8
            nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(64*8*8,128),
            nn.ReLU(),
            nn.Linear(128,10)
        )
    def forward(self,x):
        x = x.to("cpu")
        x = x.reshape(-1,1,28,28)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(x.size(0),-1)
        x = self.fc(x)
        return x


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attack_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
