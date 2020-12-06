from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image , ImageFilter , ImageDraw 
import numpy as np
import logging
logger = logging.getLogger('gunicorn.error')

class CIVE():

    def __init__(self):
        print("CIVE initialized!!")
        # self.config = FilterRunConfig()

    def predictMask(self, image, cive_r=0.441 ,cive_g=0.811, cive_b=0.385 ,cive_bias=18.78745, threshold=30):
        image = image.convert('RGB')
        r, g, b = image.split()
        cive = cive_r  * np.array(r) - cive_g * np.array(g) +  cive_b * np.array(b) + cive_bias
        cive[cive < threshold]  = 0
        cive[cive > threshold] = 255
        cive = cive.astype('uint8')
        img = Image.fromarray(cive)
        img = img.filter(ImageFilter.MinFilter(5))
        img = img.filter(ImageFilter.MedianFilter(size=5))
        return img


model = CIVE()
