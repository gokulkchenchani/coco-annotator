from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image , ImageFilter , ImageDraw 
import numpy as np
import logging
logger = logging.getLogger('gunicorn.error')

class ExG():

    def __init__(self):
        print("ExG initialized!!")
        # self.config = FilterRunConfig()

    def predictMask(self, image, padding=50, threshold=30):
        image = image.convert('RGB')
        r, g, b = image.split()
        exg = 2 * np.array(g) -  np.array(b) - np.array(r)
        exg[exg < threshold]  = 0
        exg[exg > threshold] = 255
        exg = exg.astype('uint8')
        img = Image.fromarray(exg)
        img = img.filter(ImageFilter.MinFilter(5))
        img = img.filter(ImageFilter.MedianFilter(size=5))
        return img


model = ExG()
