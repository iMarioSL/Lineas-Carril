import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self, dropout_prob):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 32, 7)
        self.pool1 = nn.MaxPool2d(4, 4)

        self.conv2 = nn.Conv2d(32, 64, 5)
        self.pool2 = nn.MaxPool2d(2, 2)

        self.conv3 = nn.Conv2d(64, 128, 2)
        self.pool3 = nn.MaxPool2d(2, 2)

        self.conv4 = nn.Conv2d(128, 256, 1)
        self.pool4 = nn.MaxPool2d(2, 2)

        # Three fully connected layers
        self.fc1 = nn.Linear(1792, 500)
        nn.init.kaiming_normal_(self.fc1.weight)
        self.drop5 = nn.Dropout(dropout_prob)

        self.fc2 = nn.Linear(500, 255)
        nn.init.kaiming_normal_(self.fc2.weight)
        self.drop6 = nn.Dropout(dropout_prob)

        self.fc3 = nn.Linear(255, 6)
        nn.init.kaiming_normal_(self.fc3.weight)


    def forward(self, x):
        x = self.pool1(F.selu(self.conv1(x)))

        x = self.pool2(F.selu(self.conv2(x)))

        x = self.pool3(F.selu(self.conv3(x)))

        x = self.pool4(F.selu(self.conv4(x)))

        # Aplanar
        x = x.view(x.size(0), -1)

        x = F.relu(self.fc1(x))
        x = self.drop5(x)

        x = F.relu(self.fc2(x))
        x = self.drop6(x)

        x = F.relu(self.fc3(x))

        return x
