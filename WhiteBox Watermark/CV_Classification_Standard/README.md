


面向深度学习图像分类模型的白盒水印加注和版权认证过程如下：

CV_Classification_Standard 目录是对图像分类深度学习模型进行白盒水印保护时用户提交文件制定的规范

我们以 cifar10 数据集和 ResNet 网络结构为例，对用户提交数据的格式进行了规定

每个文件的作用如下：

train.ipynb：训练出分类模型 ResNet.pkl、神经网络中间层数据提取模型 ResNet_Extract.pkl 以及验证模型 ResNet_Verify.pkl，都存放在了 model 目录下

WhiteBoxVerify.py：用户使用版权认证中心分发的白盒水印数据 (存放在 data 目录下) 训练并添加完水印后，向中心提交的验证模型的类定义文件

WhiteBoxExtract.py：用户在获取到疑似侵权模型的白盒权限后，针对侵权模型在用户本地构建一个神经网络中间层提取模型，向中心提交的中间层提取模型的类定义文件

WhiteBoxTest.py：版权认证中心根据用户提交的 python 文件、疑似侵权模型和用户的白盒水印数据，对模型的版权进行认证裁决

