arch = [
    (7,64,2,3),
    'M',
    (3,192,1,1),
    'M',
    (1,128,1,0),
    (3,256,1,1),
    (1,256,1,0),
    (3,512,1,1),
    'M',
    [(1,256,1,0), (3,512,1,1),4],
    (1,512,1,0),
    (3,1024,1,1),
    'M',
    [(1,512,1,0),(3,1024,1,1),2],
    (3,1024,1,1,),
    (3,1024,2,1,),
    (3,1024,1,1,),
    (3,1024,1,1,),
    
    
]
import torch.nn as nn
class CNNblock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNblock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(.1)
        
    def forward(self, x):
        return self.leakyrelu(self.batchnorm(self.conv(x)))

class Yolov1(nn.Module):
    def __init__(self, in_channels=3, **kwargs):
        super(Yolov1, self).__init__()
        
        self.architecture = arch
        self.in_channels = in_channels
        self.darknet = self.darknet_conv_net(self.architecture)
        self.fcs = self.create_FC(**kwargs)
        
    def forward(self, x):
        x = self.darknet(x)
        return self.fcs(torch.flatten(x, start_dim = 1))
    
    def darknet_conv_net(self, architecture):
        layers = []
        in_channels = self.in_channels
        
        for x in architecture:
            if type(x) == tuple:
                layers += [
                    CNNblock(in_channels, x[1], kernel_size=x[0], stride=x[2], padding=x[3])
                ]
#             print(x)
                in_channels = x[1]
    
            elif type(x) == str:
                layers += [nn.MaxPool2d(kernel_size=(2,2), stride=(2,2))]
                
            elif type(x) == []:
                conv1 = x[0]
                conv2 = x[1]
                num_repeats = x[2]
                
                for _ in range(num_repeats):
                    layers += [
                        CNNblock(in_channels, conv1[1], kernel_size=conv1[0], stride = conv1[2], padding = conv1[3])
                    ]
                    layers += [
                        CNNblock(conv1[1], conv2[1], kernel_size=conv2[0], stride = conv2[2], padding = conv2[3])
                                              
                    ]
                    
                    in_channels = conv2[1]
                    
        return nn.Sequential(*layers)
    
    def create_FC(self, split_size, num_boxes, num_classes):
        S, B, C = split_size, num_boxes, num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024*S*S, 4096),
            nn.LeakyReLU(),
            nn.Linear(4096, S*S*(C+B*5))
        )
    
    