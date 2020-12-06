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

    def exgIndex(self, image, up_thershold=10):
        # print(image.getbands(), flush=True) 
        r, g, b = image.split()
        exg = 2 * np.array(g) -  np.array(b) - np.array(r)
        exg[exg < 0]  = 0
        exg[exg > up_thershold] = 255
        exg = exg.astype('uint8')
        img = Image.fromarray(exg)
        img = img.filter(ImageFilter.MinFilter(5))
        img = img.filter(ImageFilter.MedianFilter(size=5))
        return img

    def predict_mask(self, image):

        image = image.convert('RGB')
        result = self.exgIndex(image)

        return result


model = ExG()
