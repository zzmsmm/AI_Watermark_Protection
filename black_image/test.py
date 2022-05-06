import torchvision.transforms as transforms
import cv2
trans=transforms.Compose([transforms.ToTensor()])


# img = cv2.imread('./w1_28.png')
img = cv2.imread('./w1_28.png', cv2.IMREAD_GRAYSCALE) # 使用 opencv读取图像
# img = cv2.resize('./w1_28.png', (28,28)) # 图
print(img.shape)   # numpy数组格式为（H,W,C）

transf = transforms.ToTensor()
img_tensor = transf(img)  # tensor数据格式是torch(C,H,W)
print(img_tensor.size())
img_tensor.resize_(784,1)
print(img_tensor.size())

# a=trans(img)
# b=np.array(a)  #b.shape  (1,64,64)
# maxi=b.max()
# b=b*255./maxi
# b=b.transpose(1,2,0).astype(np.uint8)
# b=np.squeeze(b,axis=2)
# xx=Image.fromarray(b)
# xx
