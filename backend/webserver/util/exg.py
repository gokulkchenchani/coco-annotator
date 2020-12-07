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
        # print(image.getbands(), flush=True)
        r, g, b = image.split()
        exg = 2 * np.array(g).astype('int32') -  np.array(b).astype('int32') - np.array(r).astype('int32')
        exg[exg < threshold]  = 0
        exg[exg > threshold] = 255
        exg = exg.astype('uint8')
        img = Image.fromarray(exg)
        return img


model = ExG()
