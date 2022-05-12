# 本文件首先训练了一个基于 cifar10 数据集的 ResNet 神经网络进行图像分类，
# 并在原始的网络中嵌入了基于二维码的水印信息
# 我们将 Verify 模块和带有水印的神经网络模型分别保存在了两个 class 中，
# 代码的后半部分有基于上述两个 class 的验证过程，从 load 模型开始。

# import packages
import torch
import torchvision

# Device configuration.
device = torch.device('cuda:2' if torch.cuda.is_available() else 'cpu')

# Transform configuration and data augmentation.
transform_train = torchvision.transforms.Compose([torchvision.transforms.Pad(4),
                                                 torchvision.transforms.RandomHorizontalFlip(),
                                                 torchvision.transforms.RandomCrop(32),
                                                 torchvision.transforms.ToTensor(),
                                                 torchvision.transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
transform_test = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                                torchvision.transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

# Hyper-parameters
num_classes = 10
batch_size = 100
learning_rate = 0.001
num_epochs = 2

# Load downloaded dataset.
train_dataset = torchvision.datasets.CIFAR10('./data', download=False, train=True, transform=transform_train)
test_dataset = torchvision.datasets.CIFAR10('./data', download=False, train=False, transform=transform_test)

# Data Loader.
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

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

# Define ResNet-18
# This class is not used to save, it is used to make another two classes to save.
class ResNet(torch.nn.Module):
    def __init__(self, block, layers, num_classes):
        super(ResNet, self).__init__()
        self.in_channels = 16
        self.conv = conv3x3(3, 16)
        self.conv_verify = conv3x3(3,16)
        self.bn = torch.nn.BatchNorm2d(16)
        self.relu = torch.nn.ReLU(inplace=True)
        self.layer1 = self._make_layers(block, 16, layers[0])
        self.layer2 = self._make_layers(block, 32, layers[1], 2)
        self.layer3 = self._make_layers(block, 64, layers[2], 2)
        self.layer4 = self._make_layers(block, 128, layers[3], 2)
        self.avg_pool = torch.nn.AdaptiveAvgPool2d((1, 1))
        self.fc = torch.nn.Linear(128, num_classes)
        self.n_input = 1*16*28*28 + 1*32*14*14 + 1*64*7*7 + 1*128*4*4
        self.fc_verify = torch.nn.Linear(self.n_input,2)
        
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
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

    def verify(self, x):
        out = self.conv_verify(x)
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
        out = self.fc_verify(z)
        return out

      
import torch.utils.data as Data
from torch.utils.data import Dataset
from PIL import Image
n = 200

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

qrdataset=QRDataset("./data/newqr/200_28/index.txt",torchvision.transforms.ToTensor())
qr_host=QRDataset("./data/newqr/200_28/index_1.txt",torchvision.transforms.ToTensor())
qr_steal=QRDataset("./data/newqr/200_28/index_2.txt",torchvision.transforms.ToTensor())
# qr_host,qr_steal=torch.utils.data.random_split(qrdataset,[int(n),int(n)])
qr_host_loader=Data.DataLoader(
    dataset=qr_host,
    batch_size=16,
    shuffle=True    
)
qr_steal_loader=Data.DataLoader(
    dataset=qr_steal,
    batch_size=16,
    shuffle=True    
)


# Make model.
model = ResNet(ResidualBlock, [2, 2, 2, 2], num_classes).to(device)

# Loss ans optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# For updating learning rate.
def update_lr(optimizer, lr):
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

        
# Train the model.
total_step = len(train_loader)
curr_lr = learning_rate
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        
        # Forward pass.
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (i+1) % 100 == 0:
            print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, total_step, loss.item()))
    # Decay learning rate.
    if (epoch+1) % 20 == 0:
        curr_lr /= 3
        update_lr(optimizer, curr_lr)

        
        
# Create a new class to save
class ResNet_s(torch.nn.Module):
    def __init__(self, block, layers, num_classes):
        super(ResNet_s, self).__init__()
        self.in_channels = 16
        self.conv = conv3x3(3, 16)
        # self.conv_verify = conv3x3(1,16)
        self.bn = torch.nn.BatchNorm2d(16)
        self.relu = torch.nn.ReLU(inplace=True)
        self.layer1 = self._make_layers(block, 16, layers[0])
        self.layer2 = self._make_layers(block, 32, layers[1], 2)
        self.layer3 = self._make_layers(block, 64, layers[2], 2)
        self.layer4 = self._make_layers(block, 128, layers[3], 2)
        self.avg_pool = torch.nn.AdaptiveAvgPool2d((1, 1))
        self.fc = torch.nn.Linear(128, num_classes)
        # self.fc_verify = torch.nn.Linear(128,2)
        
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
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out
      
      
      
model2 = ResNet_s(ResidualBlock, [2, 2, 2, 2], num_classes)
model2.conv = model.conv.cpu()
model2.bn = model.bn.cpu()
model2.relu = model.relu.cpu()
model2.layer1 = model.layer1.cpu()
model2.layer2 = model.layer2.cpu()
model2.layer3 = model.layer3.cpu()
model2.layer4 = model.layer4.cpu()
model2.avg_pool = model.avg_pool.cpu()
model2.fc = model.fc.cpu()


# Test the model.
model2.to(device)
model2.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model2(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
    print('Accuracy of the model2 on the test images: {} %'.format(100 * correct / total))

    
torch.save(model2.cpu(), './model/ResNet.pkl')


model2.to(device)


# Embedding the watermark
import copy
import time
from torch.optim import Adam,SGD
import torch.nn as nn
num_epochs_2 = 100
DA_flag = True
l=0.3

txt_path = "./data/newqr/200_28/index.txt"
fh = open(txt_path, 'r')
imgs = []
for line in fh:
    line.rstrip()
    words= line.split()
    imgs.append((words[0], int(words[1])))

copy_layer1 = []
for param in model.layer1.parameters():
    temp=copy.deepcopy(param)
    copy_layer1.append(temp)
copy_layer2 = []
for param in model.layer2.parameters():
    temp=copy.deepcopy(param)
    copy_layer2.append(temp)
copy_layer3 = []
for param in model.layer3.parameters():
    temp=copy.deepcopy(param)
    copy_layer3.append(temp)
copy_layer4 = []
for param in model.layer4.parameters():
    temp=copy.deepcopy(param)
    copy_layer4.append(temp)

loss_function=nn.CrossEntropyLoss()

for epoch in range(num_epochs_2):
    if (epoch % 10 == 0):
        print("Watermark embedding, epoch = %i in %i"% (epoch,num_epochs_2))
    time_start=time.process_time()
    if (epoch>(num_epochs_2*0.25) and (epoch%10)==0 and DA_flag):
        step,(ptb_x,ptb_y)=next(enumerate(train_loader))
        ptb_x=ptb_x.to(device)
        ptb_y=ptb_y.to(device)
        model_=copy.deepcopy(model)
        optimizer_=Adam(model_.parameters(),lr=0.0003)
        op=model_(ptb_x)
        loss=loss_function(op,ptb_y)
        optimizer_.zero_grad()
        loss.backward()
        optimizer_.step()
        for i in range(10):
            for step,(b_x,b_y) in enumerate(qr_host_loader):
                b_x=b_x.to(device)
                b_y=b_y.to(device)
                op=model.verify(b_x)
                loss=loss_function(op,b_y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
    else:  
        for step,(b_x,b_y) in enumerate(qr_host_loader):
            b_x=b_x.to(device)
            b_y=b_y.to(device)
            op=model.verify(b_x)
            loss=loss_function(op,b_y)
            if (copy_layer1 != []):
                temp=0
                for param in model.layer1.parameters():
                    loss=loss+l*torch.sum((param-copy_layer1[temp])**2)
                    temp=temp+1
            if (copy_layer2 != []):
                temp=0
                for param in model.layer2.parameters():
                    loss=loss+l*torch.sum((param-copy_layer2[temp])**2)
                    temp=temp+1
            if (copy_layer3 != []):
                temp=0
                for param in model.layer3.parameters():
                    loss=loss+l*torch.sum((param-copy_layer3[temp])**2)
                    temp=temp+1
            if (copy_layer1 != []):
                temp=0
                for param in model.layer4.parameters():
                    loss=loss+l*torch.sum((param-copy_layer4[temp])**2)
                    temp=temp+1
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    if (epoch % 10 == 0):
        error_count = 0
        for index in range(n):
            fn, label = imgs[index]
            img = Image.open(fn).convert('RGB') 
            img = torchvision.transforms.ToTensor()(img)
            img = torch.unsqueeze(img,0)
            # print(img.size())
            img = img.to(device)
            ans = model.verify(img)
            if torch.argmax(ans) != label:
                error_count=error_count+1
        print(error_count/n*100.0) 
        
        
model.to(device)


error_count=0
for step,(b_x,b_y) in enumerate(qr_host_loader):
    b_x=b_x.to(device)
    b_y=b_y.to(device)
    ans=model.verify(b_x)
    for i in range(len(b_y)):
        # print(ans)
        if torch.argmax(ans[i])!=b_y[i]:
          error_count=error_count+1
print(error_count/n*100.0)  


# 再计算一次精度
txt_path = "./data/newqr/200_28/index.txt"
fh = open(txt_path, 'r')
imgs = []
for line in fh:
    line.rstrip()
    words= line.split()
    imgs.append((words[0], int(words[1])))

error_count = 0
for index in range(n):
    fn, label = imgs[index]
    img = Image.open(fn).convert('RGB') 
    img = torchvision.transforms.ToTensor()(img)
    img = torch.unsqueeze(img,0)
    # print(img.size())
    img = img.to(device)
    ans = model.verify(img)
    # print(label)
    if torch.argmax(ans) != label:
        error_count=error_count+1
print(error_count/n*100.0)  


# Test the model.
model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
    print('Accuracy of the model on the test images: {} %'.format(100 * correct / total))

    
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
      
      
      
class Verify(torch.nn.Module):
    def __init__(self):
        super(Verify, self).__init__()
        self.n_input = 1*16*28*28 + 1*32*14*14 + 1*64*7*7 + 1*128*4*4
        self.fc_verify = torch.nn.Linear(self.n_input,2)
    def forward(self, x):
        return self.fc_verify(x)
      
      
model3 = Extract(ResidualBlock, [2, 2, 2, 2])
model3.conv = model.conv_verify.cpu()
model3.bn = model.bn.cpu()
model3.relu = model.relu.cpu()
model3.layer1 = model.layer1.cpu()
model3.layer2 = model.layer2.cpu()
model3.layer3 = model.layer3.cpu()
model3.layer4 = model.layer4.cpu()


model4 = Verify()
model4.fc_verify = model.fc_verify.cpu()


# Test the model.
model3.to(device)
# model3.eval()
model4.to(device)
error_count=0
for step,(b_x,b_y) in enumerate(qr_host_loader):
    b_x=b_x.to(device)
    b_y=b_y.to(device)
    ans=model4(model3(b_x).to(device))
    for i in range(len(b_y)):
        if torch.argmax(ans[i])!=b_y[i]:
            error_count=error_count+1
print(error_count/n*100.0)  


# Save the model
torch.save(model3.cpu(), './model/ResNet_extract.pkl')
torch.save(model4.cpu(), './model/ResNet_verify.pkl')


