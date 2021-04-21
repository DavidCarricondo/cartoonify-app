import time
import os

import numpy as np
from PIL import Image

import torch
import torchvision.transforms as transforms
from torch.autograd import Variable

from src.Transformer import Transformer

class CARTOON:
    def __init__(self):
        return None

    @staticmethod
    def _image_preprocess(image, load_size=450, gpu=-1):
        
        input_image = Image.open(image).convert('RGB')
        h, w = input_image.size

        ratio = h * 1.0/w

        if ratio > 1:
            h = load_size
            w = int(h * 1.0 / ratio)
        else:
            w = load_size
            h = int(w * ratio)

        input_image = input_image.resize((h, w), Image.BICUBIC)
        input_image = np.asarray(input_image)

        input_image = input_image[: , :, [2, 1, 0]]
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)

        input_image = -1 + 2 * input_image

        return input_image

    @staticmethod
    def _image_postprocess(image):

        output_image = image[[2, 1, 0], :, :]
        output_image = output_image.data.cpu().float() * 0.5 + 0.5

        output_image = output_image.numpy()

        output_image = np.uint8(output_image.transpose(1,2,0) * 255)
        output_image = Image.fromarray(output_image)

        return output_image
    
    def fit(self, model_path):
        model = Transformer()
        model.load_state_dict(torch.load(model_path))
        self.model = model.eval()
        return self
        
    def transform(self, image, load_size=450, gpu=-1):
        
        try:
            self.model
        except:
            raise Exception('Model has not been fit')

        if gpu > -1:
            self.model.cuda()
        else:
            self.model.float()

        input_image = self._image_preprocess(image)

        if gpu > -1:
            input_image = Variable(input_image).cuda()
        else:
            input_image = Variable(input_image).float()

        t0 = time.time()
        with torch.no_grad():
            output_image = self.model(input_image)[0]
        print(f"Inference time took {time.time() - t0} s")

        output_image = self._image_postprocess(output_image)

        return output_image

    def fit_transform(self, model_path, image):
        self.fit(model_path)
        output = self.transform(image)
        return output