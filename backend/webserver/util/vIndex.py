import numpy as np                                 
from skimage import measure                        
from shapely.geometry import Polygon, MultiPolygon 
from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image , ImageFilter , ImageDraw, ImageOps
import numpy as np
import logging
import cv2

class vIndex():

    def __init__(self):
        print("V-Index initialized!!")
        # 0: exg, 1:exgr, 2:cive
        self.filter_type = 0
        self.min_area = 100
        self.exg_threshold = 30

        self.exgr_const = 1.4
        self.exgr_threshold = 30

        self.cive_r = 0.441
        self.cive_g = 0.811
        self.cive_b = 0.385
        self.cive_bias = 18.78745
        self.cive_threshold = 30

    def exg(self, image):
        exg = 2 * np.array(self.g).astype('int32') -  np.array(self.b).astype('int32') - np.array(self.r).astype('int32')
        exg[exg < self.exg_threshold]  = 0
        exg[exg > self.exg_threshold] = 255
        exg = Image.fromarray(exg)
        return exg

    def exgr(self, image):
        exg = 2 * np.array(self.g).astype('int32') -  np.array(self.b).astype('int32') - np.array(self.r).astype('int32')
        exg[exg < self.exg_threshold]  = 0
        exg[exg > self.exg_threshold] = 255
        print(type(exg), self.exgr_const, type(np.array(self.r).astype('int32')), flush=True )
        exgr = exg - (self.exgr_const * np.array(self.r).astype('int32') - np.array(self.g).astype('int32'))
        exgr[exgr < self.exgr_threshold] = 0
        exgr[exgr > self.exgr_threshold] = 255
        exgr = Image.fromarray(exgr)
        return exgr

    def cive(self, image):
        cive = self.cive_r  * np.array(self.r).astype('int32') - self.cive_g * np.array(self.g).astype('int32') +  self.cive_b * np.array(self.b).astype('int32') + self.cive_bias
        cive[cive < self.cive_threshold]  = 0
        cive[cive > self.cive_threshold] = 255
        cive = cive.astype('uint8')
        cive = Image.fromarray(cive)
        cive = ImageOps.invert(cive)
        return cive

    def detectObjects(self, msk, category="unknow"):
        polys = im.Mask(msk).polygons()
        points = [
                np.array(point).reshape(-1, 2).round().astype(int)
                for point in polys
            ]
        coco_image = im.Image(width=self.width, height=self.height)
        for i in range(len(points)):
            mask = np.zeros((self.height, self.width))
            mask = cv2.fillPoly(mask, np.array([points[i]]), 1)
            mask = im.Mask(mask)
            if mask.area() > self.min_area:
                class_name = 'unknown'
                category = im.Category(class_name)
                coco_image.add(mask, category=category)
            else:
                print("Area < thershold!! -> not included ")
        return coco_image

    def predictMask(self, image, filter_type=0,
                                min_area=100,
                                exg_threshold=30,
                                exgr_const=1.4,  
                                exgr_threshold=30,
                                cive_r=0.441,
                                cive_g=0.811,
                                cive_b=0.385,
                                cive_bias=18.78745,
                                cive_threshold=30):

        self.filter_type = filter_type
        self.min_area = min_area
        self.exg_threshold = exg_threshold
        self.exgr_const = exgr_const
        self.exgr_threshold = exgr_threshold
        self.cive_r = cive_r
        self.cive_g = cive_g
        self.cive_b = cive_b
        self.cive_bias = cive_bias
        self.cive_threshold = cive_threshold


        image = image.convert('RGB')
        self.r, self.g, self.b = image.split()
        print(self.r, self.g, self.b,flush=True)
        self.width, self.height = image.size
        # print(image.getbands(), flush=True)
        
        if self.filter_type == 0:
            msk = self.exg(image)

        elif self.filter_type == 1:
            msk = self.exgr(image)
        
        elif self.filter_type == 2:
            msk = self.cive(image)
 
        else:
            print("Invalid filter Type!!!", flush=True)
            return

        coco_image = self.detectObjects(msk)

        return coco_image.coco()

model = vIndex()
