import os
import torch
from model import U2NET # full size version 173.6 MB
from model import U2NETP # small version u2net 4.7 MB


def model(model_name='u2net'):

 
    model_dir = os.path.join(os.getcwd(),'U-2-Net','saved_models', model_name, model_name + '.pth')

    if(model_name=='u2net'):
        print("...load U2NET---173.6 MB")
        net = U2NET(3,1)
    elif(model_name=='u2netp'):
        print("...load U2NEP---4.7 MB")
        net = U2NETP(3,1)
    net.load_state_dict(torch.load(model_dir))
    # net.load_state_dict(torch.load(model_dir, map_location=torch.device('cpu')))

    if torch.cuda.is_available():
        net.cuda()
    net.eval()

    return net
