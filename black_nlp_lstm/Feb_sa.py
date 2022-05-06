import torch
import torchtext
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.utils.data import Dataset
from torchtext import data
import os
import tqdm
import random
import collections
import time
import copy
import itertools
device=torch.device("cuda:0")
N=200
random.seed(7)
torch.manual_seed(7)
torch.cuda.manual_seed_all(7)

class WMDataset(Dataset):
    def __init__(self,N):
        self.N=N
        sentences=[]
        for i in range(2*N):
            sentence=[]
            for j in range(500):
                w=int(random.uniform(10000,20000))
                sentence.append(w)
            sentences.append(torch.tensor(sentence))
        self.sentences=sentences
    def __getitem__(self,index):
        label=int(index%2)
        s=self.sentences[index]
        return s,label
    def __len__(self):
        return len(self.sentences)

def read_imdb(folder,data_root):
    data=[]
    for label in ["pos","neg"]:
        folder_name=os.path.join(data_root,folder,label)
        for file in os.listdir(folder_name):
            with open(os.path.join(folder_name,file),"rb") as f:
                review=f.read().decode("utf-8").replace("\n","").lower()
                data.append([review,1 if label=="pos" else 0])
    random.shuffle(data)
    return data
data_root="./.data/imdb/aclImdb"
train_data,test_data=read_imdb("train",data_root),read_imdb("test",data_root)

for sample in train_data[:5]:
    print(sample[1],"\t",sample[0][:50])

def get_tokenized_imdb(data):
    def tokenizer(text):
        return [tok.lower() for tok in text.split(" ")]
    return [tokenizer(review) for review,_ in data]
def get_vocab_imdb(data):
    tokenized_data=get_tokenized_imdb(data)
    counter=collections.Counter([tk for st in tokenized_data for tk in st])
    return torchtext.vocab.Vocab(counter,min_freq=5)

vocab=get_vocab_imdb(train_data)
print(len(vocab))

def preprocess_imdb(data,vocab):
    max_l=500
    def pad(x):
        return x[:max_l] if len(x)>max_l else x+[0]*(max_l-len(x))
    tokenized_data=get_tokenized_imdb(data)
    features=torch.tensor([pad([vocab.stoi[word] for word in words]) for words in tokenized_data])
    labels=torch.tensor([score for _,score in data])
    return features,labels
train_set=Data.TensorDataset(*preprocess_imdb(train_data,vocab))
test_set=Data.TensorDataset(*preprocess_imdb(test_data,vocab))
batch_size=64
train_iter=Data.DataLoader(train_set,batch_size,shuffle=True)
test_iter=Data.DataLoader(test_set,batch_size)
for X,y in train_iter:
    print("X",X.shape,"y",y.shape)
    break
print("#batches",len(train_iter))

class MyLSTM(nn.Module):
    def __init__(self,vocab,embed_size,num_hiddens,num_layers,test_iter,wm_iter):
        super(MyLSTM,self).__init__()
        self.test_iter=test_iter
        self.embedding=nn.Embedding(len(vocab),embed_size)
        self.encoder=nn.LSTM(input_size=embed_size,
                             hidden_size=num_hiddens,
                             num_layers=num_layers,
                             bidirectional=True)
        self.decoder=nn.Linear(4*num_hiddens,2)
        self.cwm=nn.Sequential(
                 nn.Linear(18*num_hiddens,60),
                 nn.ReLU(),
                 nn.Linear(60,2))
        self.cha=nn.Sequential(
                 nn.Linear(18*num_hiddens,60),
                 nn.ReLU(),
                 nn.Linear(60,2))
        self.wm_iter=wm_iter
    def forward(self,inputs):
        embeddings=self.embedding(inputs.permute(1,0))
        outputs,_=self.encoder(embeddings)
        encoding=torch.cat((outputs[0],outputs[-1]),-1)
        outs=self.decoder(encoding)
        return outs
    def wm(self,inputs):
        embeddings=self.embedding(inputs.permute(1,0))
        a,(b,c)=self.encoder(embeddings)
        op=torch.cat((a[50],a[150],a[250],a[350],a[450],b[0],b[1],b[2],b[3],c[0],c[1],c[2],c[3]),-1)
        z=self.cwm(op)
        return z
    def hack(self,inputs):
        embeddings=self.embedding(inputs.permute(1,0))
        a,(b,c)=self.encoder(embeddings)
        op=torch.cat((a[50],a[150],a[250],a[350],a[450],b[0],b[1],b[2],b[3],c[0],c[1],c[2],c[3]),-1)
        z=self.cha(op)
        return z

    def test(self):
        acc_sum=0.0
        n=0
        for X,y in self.test_iter:
            X=X.to(device)
            y=y.to(device)
            y_hat=self.forward(X)
            acc_sum+=(y_hat.argmax(dim=1)==y).sum().cpu().item()
            n+=y.shape[0]
        return acc_sum/n
    def wm_acc(self):
        acc_sum=0.0
        n=0
        for X,y in self.wm_iter:
            X=X.to(device)
            y=y.to(device)
            y_hat=self.wm(X)
            acc_sum+=(y_hat.argmax(dim=1)==y).sum().cpu().item()
            n+=y.shape[0]
        return (n-acc_sum)/n*100

wm=WMDataset(N)
wm_loader=Data.DataLoader(dataset=wm,batch_size=64,shuffle=True)
myLSTM=MyLSTM(vocab,100,100,2,test_iter,wm_loader)
glove_vocab=torchtext.vocab.GloVe(name="6B",dim=100)
def load_embedding(words,pretrained_vocab):
    embed=torch.zeros(len(words),pretrained_vocab.vectors[0].shape[0])
    oov_count=0
    for i,word in enumerate(words):
        try:
            idx=pretrained_vocab.stoi[word]
            embed[i,:]=pretrained_vocab.vectors[idx]
        except KeyError:
            oov_count+=1
    if oov_count>0:
        print("%d oov words." % oov_count)
    return embed

myLSTM.embedding.weight.data.copy_(load_embedding(vocab.itos,glove_vocab))
myLSTM.embedding.weight.requires_grad=False
myLSTM=myLSTM.to(device)
#print("Load wm.")
#print(myLSTM.wm_acc())

def train(train_iter,test_iter,net,loss,optimizer,device,num_epochs):
    net=net.to(device)
    print("Training on",device)
    batch_count=0
    for epoch in range(num_epochs):
        train_l_sum,train_acc_sum,n,start=0.0,0.0,0,time.time()
        for X,y in train_iter:
            X=X.to(device)
            y=y.to(device)
            y_hat=net(X)
            l=loss(y_hat,y)
            optimizer.zero_grad()
            l.backward()
            optimizer.step()
            train_l_sum+=l.cpu().item()
            train_acc_sum+=(y_hat.argmax(dim=1)==y).sum().cpu().item()
            n+=y.shape[0]
            batch_count+=1
        test_acc=myLSTM.test()
        print("Epoch %d, loss %.4f, train acc %.3f, test acc %.3f, time %.1f sec" % (epoch+1,train_l_sum/batch_count,train_acc_sum/n,test_acc,time.time()-start))
    torch.save(net.state_dict(), 'white.pt')
def wm_train(net,loss,optimizer,device,num_epochs):
    net=net.to(device)
    for epoch in range(num_epochs):
        for X,y in net.wm_iter:
            X=X.to(device)
            y=y.to(device)
            y_hat=net.wm(X)
            l=loss(y_hat,y)
            optimizer.zero_grad()
            l.backward()
            optimizer.step()
        if (epoch%20==0):
            print("Epoch %d, wm acc %.3f" %(epoch+1,net.wm_acc()))
    torch.save(net.state_dict(), 'white.pt')

embed_history=[]
embed_test=[]
lr,num_epochs=0.002,15
optimizer=torch.optim.Adam(filter(lambda p:p.requires_grad,myLSTM.parameters()),lr=lr)

DA=False
#Varying l
#optimizer_=torch.optim.Adam(myLSTM.cwm.parameters,lr=0.001)
optimizer_=torch.optim.Adam([p for p in myLSTM.parameters() if p.requires_grad],lr=0.001)
loss=nn.CrossEntropyLoss()
train(train_iter,test_iter,myLSTM,loss,optimizer,device,num_epochs)
myLSTM=myLSTM.to(device)
for epoch in range(200):
    if (epoch>100) and (epoch%20==0) and DA:
        mm=copy.deepcopy(myLSTM)
        mm_optimizer=torch.optim.Adam(mm.parameters(),lr=0.002)
        train(train_iter,test_iter,mm,loss,mm_optimizer,device,1)
        for cc in range(10):
            for X,y in myLSTM.wm_iter:
                X=X.to(device)
                y=y.to(device)
                embeddings=mm.embedding(X.permute(1,0))
                a,(b,c)=mm.encoder(embeddings)
                op=torch.cat((a[50],a[150],a[250],a[350],a[450],b[0],b[1],b[2],b[3],c[0],c[1],c[2],c[3]),-1)
                z=myLSTM.cwm(op)
                l=loss(z,y)
                optimizer_.zero_grad()
                l.backward()
                optimizer_.step()
    for X,y in myLSTM.wm_iter:
        X=X.to(device)
        y=y.to(device)
        y_hat=myLSTM.wm(X)
        l=loss(y_hat,y)
        optimizer_.zero_grad()
        l.backward()
        optimizer_.step()
    embed_history.append(myLSTM.wm_acc())
    if (epoch%10==0):
        print("Epoch %d, wm acc %.3f"%(epoch+1,myLSTM.wm_acc()))
        k=myLSTM.test()
        print(k)
        embed_test.append(k)
ft_history=[]
for epoch in range(10):
    train(train_iter,test_iter,myLSTM,loss,optimizer,device,1)
    ft_history.append(myLSTM.wm_acc())
    print("FT epoch %d, wm acc %.3f"%(epoch+1,myLSTM.wm_acc()))
torch.save(myLSTM.state_dict(), 'white.pt')
print(embed_history)
print(embed_test)
print(ft_history)

