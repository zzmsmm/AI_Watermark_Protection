## 针对深度学习中CV模型的白盒水印加注和版权认证流程
参考论文：https://arxiv.org/abs/2103.10021
### 概述

我们基于 PyTorch 和 Python 制定了针对深度学习中CV模型的白盒水印加注和版权认证规范，用户按照我们网站的规范，在本地训练自己的模型，将水印数据加注到事先训练好的深度学习模型中，并按照要求提交相关文件后，即可完成对其模型的版权认证。当用户面对侵权行为时，登录我们的网站并按要求提交相关文件后，我们的网站会根据后门数据对提交模型的侵权程度作出裁决，并为用户提供一个不具备法律效力的裁决结果。

### 水印加注算法
算法的步骤如下：
1. 首先由我们的网站（即版权认证中心）根据用户的身份、提交的模型、提交的时间等信息为用户生成专用于该模型的二维码和分类结果

算法原理图如下：
![mtl](https://user-images.githubusercontent.com/72694643/168418071-8bcdb94e-1170-40a7-a321-eb43fd0daf8c.png)





### 文件提交规范和版权认证流程
#### 图像分类模型

CV_Classification_Standard 目录是对深度学习中图像分类模型进行白盒水印保护时用户提交文件制定的规范

我们以 cifar10 数据集和 ResNet 网络结构为例，对用户提交数据的格式进行了规定

每个文件的作用如下：

train.ipynb：利用数据集训练出分类模型 ResNet.pkl、神经网络中间层数据提取模型 ResNet_Extract.pkl 以及验证模型 ResNet_Verify.pkl，存放在 model 目录下

WhiteBoxVerify.py：用户使用版权认证中心分发的白盒水印数据 (存放在 data 目录下) 训练并添加完水印后，向中心提交的验证模型的类定义文件

WhiteBoxExtract.py：用户在获取到疑似侵权模型的白盒权限后，针对侵权模型在用户本地构建一个神经网络中间层提取模型，向中心提交的中间层提取模型的类定义文件

WhiteBoxTest.py：版权认证中心根据用户提交的 python 文件、疑似侵权模型和用户的白盒水印数据，对模型的版权进行认证裁决


#### 目标检测模型
CV_ObjectDetection_Standard 目录是对深度学习中目标检测模型进行白盒水印保护时用户提交文件制定的规范

我们以 PennFudan 数据集和 ResNet 网络结构为例，对用户提交数据的格式进行了规定

每个文件的作用如下：

train.ipynb、coco_eval.py、coco_utils.py、engine.py、transforms.py、utils.py：利用预训练的 maskrcnn_resnet50_fpn 模型在 PennFudan 数据集上训练出目标检测模型











