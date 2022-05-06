import os
import numpy as np
import itertools
from engine import train_one_epoch, evaluate
import utils
import transforms as T

import torch
from PIL import Image
from gen_qr_keys import QRDataset
import copy
import itertools
import torch.nn as nn
from torch.optim import Adam
import torch.nn.functional as F
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

import torch.utils.data as Data
from torch.utils.data import Dataset
n=200
torch.manual_seed(516)
torch.cuda.manual_seed_all(516)

class PennFudanDataset(object):
    def __init__(self, root, transforms):
        self.root = root
        self.transforms = transforms
        # load all image files, sorting them to
        # ensure that they are aligned
        self.imgs = list(sorted(os.listdir(os.path.join(root, "PNGImages"))))
        self.masks = list(sorted(os.listdir(os.path.join(root, "PedMasks"))))

    def __getitem__(self, idx):
        # load images ad masks
        img_path = os.path.join(self.root, "PNGImages", self.imgs[idx])
        mask_path = os.path.join(self.root, "PedMasks", self.masks[idx])
        img = Image.open(img_path).convert("RGB")
        # note that we haven't converted the mask to RGB,
        # because each color corresponds to a different instance
        # with 0 being background
        mask = Image.open(mask_path)

        mask = np.array(mask)
        # instances are encoded as different colors
        obj_ids = np.unique(mask)
        # first id is the background, so remove it
        obj_ids = obj_ids[1:]

        # split the color-encoded mask into a set
        # of binary masks
        masks = mask == obj_ids[:, None, None]

        # get bounding box coordinates for each mask
        num_objs = len(obj_ids)
        boxes = []
        for i in range(num_objs):
            pos = np.where(masks[i])
            xmin = np.min(pos[1])
            xmax = np.max(pos[1])
            ymin = np.min(pos[0])
            ymax = np.max(pos[0])
            boxes.append([xmin, ymin, xmax, ymax])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)
        masks = torch.as_tensor(masks, dtype=torch.uint8)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)

def get_model_instance_segmentation(num_classes):
    # load an instance segmentation model pre-trained pre-trained on COCO
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # now get the number of input features for the mask classifier
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    # and replace the mask predictor with a new one
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                       hidden_layer,
                                                       num_classes)

    return model


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)

def verify_acc(model,Cwm,qr_host_loader):
    error_count=0
    for step,(b_x,b_y) in enumerate(qr_host_loader):
        b_x=b_x.to(device)
        b_y=b_y.to(device)
        z=model.backbone.body.conv1(b_x)
        z=model.backbone.body.bn1(z)
        z=model.backbone.body.relu(z)
        z=model.backbone.body.maxpool(z)
        z1=model.backbone.body.layer1(z)
        z2=model.backbone.body.layer2(z1)
        z3=model.backbone.body.layer3(z2)
        z4=model.backbone.body.layer4(z3)
        z1=F.avg_pool2d(z1,4)
        z1=z1.view(z1.size(0),-1)
        z2=F.avg_pool2d(z2,4)
        z2=z2.view(z2.size(0),-1)
        z3=F.avg_pool2d(z3,4)
        z3=z3.view(z3.size(0),-1)
        z4=F.avg_pool2d(z4,4)
        z4=z4.view(z4.size(0),-1)
        zz=torch.cat((z1,z2,z3,z4),dim=1)
        # 把四个层（ layer+平均池化 ）的输出作为 verify 模块的输入
        op=Cwm(zz)
        for i in range(len(b_y)):
            if torch.argmax(op[i])!=b_y[i]:
                error_count=error_count+1
    return error_count/n*100.0


# train on the GPU or on the CPU, if a GPU is not available
device = torch.device('cuda:1') if torch.cuda.is_available() else torch.device('cpu')

# our dataset has two classes only - background and person
num_classes = 2
# use our dataset and defined transformations
dataset = PennFudanDataset('./data/PennFudanPed', get_transform(train=True))
dataset_test = PennFudanDataset('./data/PennFudanPed', get_transform(train=False))

# split the dataset in train and test set
indices = torch.randperm(len(dataset)).tolist()
dataset = torch.utils.data.Subset(dataset, indices[:-50])
dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])

# define training and validation data loaders
data_loader = torch.utils.data.DataLoader(
    dataset, batch_size=1, shuffle=True, num_workers=0,
    collate_fn=utils.collate_fn)

data_loader_test = torch.utils.data.DataLoader(
    dataset_test, batch_size=1, shuffle=False, num_workers=0,
    collate_fn=utils.collate_fn)

qrdataset=QRDataset("./data/newqr/200_112/index.txt",torchvision.transforms.ToTensor())
qr_host,qr_steal=torch.utils.data.random_split(qrdataset,[int(n),int(n)],generator=torch.Generator().manual_seed(4396))
qr_host_loader=Data.DataLoader( dataset=qr_host,
                                batch_size=30,
                                shuffle=True)
qr_steal_loader=Data.DataLoader(dataset=qr_steal,
                                batch_size=30,
                                shuffle=True)

# get the model using our helper function
model = get_model_instance_segmentation(num_classes)

# move model to the right device
model.to(device)

# construct an optimizer
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.Adam(params, lr=0.0002,)
# and a learning rate scheduler
#lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,step_size=3,gamma=0.1)

# let's train it for 10 epochs
num_epochs = 20
for epoch in range(num_epochs):
    print("%i primary epoch in 20"% epoch)
    # train for one epoch, printing every 10 iterations
    train_one_epoch(model, optimizer, data_loader, device, epoch, 60,False)
    # update the learning rate
    # lr_scheduler.step()
    # evaluate on the test dataset
    evaluate(model, data_loader_test, device,False)

train_one_epoch(model, optimizer, data_loader, device, epoch, 60,True)
evaluate(model, data_loader_test, device,True)

Cwm=nn.Sequential(
    nn.Linear(20224,256),
    nn.ReLU(),
    nn.Linear(256,2))
Cwm=Cwm.to(device)
loss_function=nn.CrossEntropyLoss()
optimizer_=Adam(Cwm.parameters(),lr=0.0001)
conv1_p=[]
for param in model.backbone.body.conv1.parameters():
    temp=copy.deepcopy(param)
    conv1_p.append(temp)
layer1_p=[]
for param in model.backbone.body.layer1.parameters():
    temp=copy.deepcopy(param)
    layer1_p.append(param)
layer2_p=[]
for param in model.backbone.body.layer2.parameters():
    temp=copy.deepcopy(param)
    layer2_p.append(param)
layer3_p=[]
for param in model.backbone.body.layer3.parameters():
    temp=copy.deepcopy(param)
    layer3_p.append(param)
layer4_p=[]
for param in model.backbone.body.layer4.parameters():
    temp=copy.deepcopy(param)
    layer4_p.append(param)

epoch=500
DA=False
embed_history=[]
for e in range(epoch):
    va=verify_acc(model,Cwm,qr_host_loader)
    embed_history.append(va)
    if (e>epoch*0.5) and (e%50==0) and DA:
        mm=copy.deepcopy(model)
        mm=mm.to(device)
        mm_optimizer=Adam([p for p in mm.parameters() if p.requires_grad],lr=0.0002)
        train_one_epoch(mm, mm_optimizer, data_loader, device, e, 60,False)
        for ie in range(20):
            for step,(b_x,b_y) in enumerate(qr_host_loader):
                b_x=b_x.to(device)
                b_y=b_y.to(device)
                z=mm.backbone.body.conv1(b_x)
                z=mm.backbone.body.bn1(z)
                z=mm.backbone.body.relu(z)
                z=mm.backbone.body.maxpool(z)
                z1=mm.backbone.body.layer1(z)
                z2=mm.backbone.body.layer2(z1)
                z3=mm.backbone.body.layer3(z2)
                z4=mm.backbone.body.layer4(z3)
                z1=F.avg_pool2d(z1,4)
                z1=z1.view(z1.size(0),-1)
                z2=F.avg_pool2d(z2,4)
                z2=z2.view(z2.size(0),-1)
                z3=F.avg_pool2d(z3,4)
                z3=z3.view(z3.size(0),-1)
                z4=F.avg_pool2d(z4,4)
                z4=z4.view(z4.size(0),-1)
                zz=torch.cat((z1,z2,z3,z4),dim=1)
                op=Cwm(zz)
                loss=loss_function(op,b_y)
                optimizer_.zero_grad()
                loss.backward()
                optimizer_.step()
    else:
        for step,(b_x,b_y) in enumerate(qr_host_loader):
            b_x=b_x.to(device)
            b_y=b_y.to(device)
            z=model.backbone.body.conv1(b_x)
            z=model.backbone.body.bn1(z)
            z=model.backbone.body.relu(z)
            z=model.backbone.body.maxpool(z)
            z1=model.backbone.body.layer1(z)
            z2=model.backbone.body.layer2(z1)
            z3=model.backbone.body.layer3(z2)
            z4=model.backbone.body.layer4(z3)
            z1=F.avg_pool2d(z1,4)
            z1=z1.view(z1.size(0),-1)
            z2=F.avg_pool2d(z2,4)
            z2=z2.view(z2.size(0),-1)
            z3=F.avg_pool2d(z3,4)
            z3=z3.view(z3.size(0),-1)
            z4=F.avg_pool2d(z4,4)
            z4=z4.view(z4.size(0),-1)
            zz=torch.cat((z1,z2,z3,z4),dim=1)
            op=Cwm(zz)
            loss=loss_function(op,b_y)
            optimizer_.zero_grad()
            loss.backward()
            optimizer_.step()
    if (e%100==0):
        print("Accuracy=%f, %i in %i epochs"%(verify_acc(model,Cwm,qr_host_loader),e,epoch))
        print(loss)
        #evaluate(model,data_loader_test,device,True)
print("Embedding terminates.-------------------------------------------------------------")
evaluate(model,data_loader_test,device,True)
print("-------------------------------------------------------------------------")
ft_record=[]

for e in range(10):
    train_one_epoch(model, optimizer, data_loader, device, e, 60,True)
    evaluate(model, data_loader_test,device, True)
    v=verify_acc(model,Cwm,qr_host_loader)
    ft_record.append(v)
    print("FT epoch %i, acc = %f" % (e,v))
    print("------------------------------------------------------------------")

print("That's it!")
print(embed_history)
print(ft_record)

