from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image , ImageFilter , ImageDraw , ImageOps
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
        cive = cive_r  * np.array(r).astype('int32') - cive_g * np.array(g).astype('int32') +  cive_b * np.array(b).astype('int32') + cive_bias
        cive[cive < threshold]  = 0
        cive[cive > threshold] = 255
        cive = cive.astype('uint8')
        img = Image.fromarray(cive)
        img = ImageOps.invert(img)
        return img


model = CIVE()
