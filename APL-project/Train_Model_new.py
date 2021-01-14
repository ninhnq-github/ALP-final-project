import pandas as pd

# load data
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# separate label and pixels for the training set
# the testing set does not contain lables
labels = train["label"]
pureimg_train = train.drop(labels = ["label"], axis = 1) # drop the label column
del train # no longer needed


# normalize train and test
norm_train = pureimg_train/255
norm_test = test/255

# split the training data into training and validation set
from sklearn.model_selection import train_test_split

feature_train, feature_validate, target_train, target_validate = train_test_split(norm_train, labels, test_size = 0.1, random_state = 0)

# feature: non-label part of the image
# target: what we want to get, so it is the label of the image
# we should not reshape just yet because this function defaultly separates data row wise by axis 0
# so the shape of 2D training data set array should be one image per row
# otherwise it will be separated incorrectly


# change data frame to numpy, and then to tensor form
# time to reshape
import numpy as np
import torch

Test = torch.from_numpy(norm_test.values.reshape((-1,1,28,28)))
featuresTrain = torch.from_numpy(feature_train.values.reshape((-1,1,28,28)))
targetsTrain = torch.from_numpy(target_train.values)
featuresValidation = torch.from_numpy(feature_validate.values.reshape((-1,1,28,28)))
targetsValidation = torch.from_numpy(target_validate.values)


import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset

# define batch size
batch_size = 378

# define own dataset
class MNISTDataset(Dataset):
    """MNIST dataset"""
    
    def __init__(self, feature, target=None, transform=None):
        
        self.X = feature
        self.y = target
            
        self.transform = transform
    
    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        # training
        if self.transform is not None:
            return self.transform(self.X[idx]), self.y[idx]
        # testing
        elif self.y is None:
            return [self.X[idx]]
        # validation
        return self.X[idx], self.y[idx]

# define transform operation
data_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomAffine(degrees=45, translate=(0.1, 0.1), scale=(0.8, 1.2)),
    transforms.ToTensor()])

# create dataset
train_set = MNISTDataset(featuresTrain.float(), targetsTrain, transform=data_transform)
validate_set = MNISTDataset(featuresValidation.float(), targetsValidation)
test_set = MNISTDataset(Test.float())


# if choose not to do data augmentation
# create dataset like this, move this cell to the end of the section before data loading
train_set = torch.utils.data.TensorDataset(featuresTrain.float(), targetsTrain)
validate_set = torch.utils.data.TensorDataset(featuresValidation.float(), targetsValidation)
test_set = torch.utils.data.TensorDataset(Test.float())


# load the data
train_loader = torch.utils.data.DataLoader(train_set, batch_size = batch_size, shuffle = True)
validate_loader = torch.utils.data.DataLoader(validate_set, batch_size = batch_size, shuffle = False)
test_loader = torch.utils.data.DataLoader(test_set, batch_size = batch_size, shuffle = False)


import torch.nn as nn

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        
        self.cnn = nn.Sequential(nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5),
                                     nn.ReLU(inplace=True),
                                     nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5),
                                     nn.ReLU(inplace=True),
                                     nn.MaxPool2d(kernel_size=2),
                                     nn.Dropout(0.25),
                                     nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
                                     nn.ReLU(inplace=True),
                                     nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3),
                                     nn.ReLU(inplace=True),
                                     nn.MaxPool2d(kernel_size=2, stride=2),
                                     nn.Dropout(0.25))
        
        self.classifier = nn.Sequential(nn.Linear(576, 256),
                                       nn.Dropout(0.5),
                                       nn.Linear(256, 10))

        
    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1) # flatten layer
        x = self.classifier(x)
        
        return x

import torch.optim as optim

# defining the model
model = CNNModel()

# set optimizer, loss function, and learning rate reduction
# all these parameter comes from the first notebook in citation, the author explains the reason of choosing well
optimizer = optim.RMSprop(model.parameters(), lr=0.001, alpha=0.9)

criterion = nn.CrossEntropyLoss()

lr_reduction = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0.00001)

if torch.cuda.is_available():
    model = model.cuda()
    criterion = criterion.cuda()


# for visualization
count = 0
loss_list = []
iteration_list = []
average_training_accuracy = []
average_validation_accuracy = []
average_training_loss = []
average_validation_loss = []


from torch.autograd import Variable

def train(epoch):
    # print('Epoch ', epoch) # uncomment me to show verbose
    global count
    model.train()

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data), Variable(target)
        
        if torch.cuda.is_available():
            data = data.cuda()
            target = target.cuda()
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        
        loss.backward()
        optimizer.step()
        
        if (batch_idx + 1)% 100 == 0:
            # store loss and iteration
            loss_list.append(loss.item())
            iteration_list.append(count)
            count += 1
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(epoch, (batch_idx + 1) * len(data), len(train_loader.dataset), 100. * (batch_idx + 1) / len(train_loader), loss.item())) # uncomment me to show verbose

import torch.nn.functional as F

def evaluate(data_loader, validate=False):
    model.eval()
    loss = 0
    correct = 0
    
    for data, target in data_loader:
        data, target = Variable(data), Variable(target)
        if torch.cuda.is_available():
            data = data.cuda()
            target = target.cuda()
        
        output = model(data)
        
        loss += F.cross_entropy(output, target, size_average=False).item()

        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        
    loss /= len(data_loader.dataset)
    
    accuracy = 100. * correct / len(data_loader.dataset)
    
    if not validate:
        lr_reduction.step(loss)
        average_training_accuracy.append(accuracy)
        average_training_loss.append(loss)
        print('Average training loss: {:.4f}, Accuracy: {}/{} ({:.3f}%)'.format(loss, correct, len(data_loader.dataset), accuracy)) # uncomment me to show verbose
    else:
        average_validation_accuracy.append(accuracy)
        average_validation_loss.append(loss)
        print('Average validation loss: {:.4f}, Accuracy: {}/{} ({:.3f}%)\n'.format(loss, correct, len(data_loader.dataset), accuracy)) # uncomment me to show verbose




import matplotlib.pyplot as plt

n_epochs = 200
# without data augmentation reaches 99.3, with augmentation reaches 99.2

for epoch in range(n_epochs):
    train(epoch)
    evaluate(train_loader)
    evaluate(validate_loader, True)

torch.save(model, 'model_new_final_1.pt')
    
plt.plot(iteration_list,loss_list)
plt.xlabel("Number of iteration")
plt.ylabel("Loss")
plt.title("Training Loss vs Number of iteration")
#plt.show()

epoch_list = [i for i in range(n_epochs)]

plt.plot(epoch_list, average_training_loss)
plt.plot(epoch_list, average_validation_loss)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss vs Epoch")
#plt.show()

plt.plot(epoch_list, average_training_accuracy)
plt.plot(epoch_list, average_validation_accuracy)
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Epoch")
#plt.show()
