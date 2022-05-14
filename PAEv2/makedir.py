import os

root1 = "CASIA-WebFace"
root2 = "WebFace-align128"

if __name__ == '__main__':
    for dir in os.listdir(root1):
        print(dir)
        os.makedirs(os.path.join(root2, dir))
