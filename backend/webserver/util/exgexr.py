from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image , ImageFilter , ImageDraw 
import numpy as np
import logging
logger = logging.getLogger('gunicorn.error')

class ExGExR():

    def __init__(self):
        print("ExGExR initialized!!")
        # self.config = FilterRunConfig()

    def predictMask(self, image, const=1.4, threshold=30):
        image = image.convert('RGB')
        r, g, b = image.split()
        exg = 2 * np.array(g).astype('int32') -  np.array(b).astype('int32') - np.array(r).astype('int32')
        exg[exg<threshold] = 0
        exg[exg>threshold] = 255
        exg = exg.astype('uint8')
        eexr = exg - (1.4 * np.array(r).astype('int32') - np.array(g).astype('int32'))
        eexr[eexr<threshold] = 0
        eexr[eexr>threshold] = 255
        img = Image.fromarray(eexr)
        return img


model = ExGExR()
