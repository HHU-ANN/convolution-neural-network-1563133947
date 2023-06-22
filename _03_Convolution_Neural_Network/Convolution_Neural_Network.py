# 在该文件NeuralNetwork类中定义你的模型 
# 在自己电脑上训练好模型，保存参数，在这里读取模型参数（不要使用JIT读取），在main中返回读取了模型参数的模型

import os

os.system("sudo pip3 install torch")
os.system("sudo pip3 install torchvision")

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as dset
import torchvision.transforms as transforms

from torch.utils.data import DataLoader
    

class NeuralNetwork(nn.Module):
    def __init__(self, num_classes=10):
        super(NeuralNetwork, self).__init__()

        # 定义卷积层和池化层
        self.conv_layer1 = nn.Conv2d(3, 64, kernel_size=3, stride=2, padding=1)
        self.relu1 = nn.ReLU(inplace=True)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv_layer2 = nn.Conv2d(64, 192, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU(inplace=True)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv_layer3 = nn.Conv2d(192, 384, kernel_size=3, padding=1)
        self.relu3 = nn.ReLU(inplace=True)

        self.conv_layer4 = nn.Conv2d(384, 256, kernel_size=3, padding=1)
        self.relu4 = nn.ReLU(inplace=True)

        self.conv_layer5 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.relu5 = nn.ReLU(inplace=True)
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        # 定义全连接层和dropout层
        self.fc1 = nn.Linear(256 * 2 * 2, 4096)
        self.relu6 = nn.ReLU(inplace=True)
        self.dropout1 = nn.Dropout()

        self.fc2 = nn.Linear(4096, 4096)
        self.relu7 = nn.ReLU(inplace=True)
        self.dropout2 = nn.Dropout()

        self.fc3 = nn.Linear(4096, num_classes)

    def forward(self, x):
        # 前向传播
        x = self.conv_layer1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        x = self.conv_layer2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)

        x = self.conv_layer3(x)
        x = self.relu3(x)

        x = self.conv_layer4(x)
        x = self.relu4(x)

        x = self.conv_layer5(x)
        x = self.relu5(x)
        x = self.maxpool3(x)

        x = x.view(x.size(0), -1)

        x = self.fc1(x)
        x = self.relu6(x)
        x = self.dropout1(x)

        x = self.fc2(x)
        x = self.relu7(x)
        x = self.dropout2(x)

        x = self.fc3(x)

        return x

transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),  # 随机水平翻转
    transforms.RandomCrop(32, padding=4),  # 随机裁剪
    transforms.ToTensor(),  # 转换为Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # 标准化
                         std=[0.229, 0.224, 0.225])
])

def read_data():
    # 这里可自行修改数据预处理，batch大小也可自行调整
    # 保持本地训练的数据读取和这里一致
    dataset_train = dset.CIFAR10(root='./data', train=True, download=True, transform=transforms.ToTensor())
    dataset_val = dset.CIFAR10(root='./data', train=False, download=True, transform=transforms.ToTensor())
    data_loader_train = DataLoader(dataset=dataset_train, batch_size=128, shuffle=True)
    data_loader_val = DataLoader(dataset=dataset_val, batch_size=100, shuffle=False)
    return dataset_train, dataset_val, data_loader_train, data_loader_val

def main():
    model = NeuralNetwork() # 若有参数则传入参数
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    model.load_state_dict(torch.load(parent_dir + '/pth/model.pth',map_location=torch.device('cpu')))
    return model
    
