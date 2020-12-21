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
        # print(type(exg), self.exgr_const, type(np.array(self.r).astype('int32')), flush=True )
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

    def pickPoly(self, mask, points):

        polys = self.getPolys(mask)

        _width = self.width//2
        _height = self.height//2

        # print(points[0]['x'], points[0]['y'],  flush=True)
        # print(points[1]['x'], points[1]['y'],  flush=True)
        # print(points[2]['x'], points[2]['y'],  flush=True)
        # print(points[3]['x'], points[3]['y'],  flush=True)
        # print(points[4]['x'], points[4]['y'],  flush=True)

        points[0]['x'] += _width
        points[1]['x'] += _width 
        points[2]['x'] += _width
        points[3]['x'] += _width 
        points[4]['x'] += _width 

        points[0]['y'] += _height
        points[1]['y'] += _height 
        points[2]['y'] += _height
        points[3]['y'] += _height 
        points[4]['y'] += _height 

        AB_vec = np.array([(points[1]['x']-points[0]['x']), (points[1]['y']-points[0]['y'])])
        AB_dot_AB = np.dot(AB_vec,AB_vec)

        idx = 0
        score = np.zeros(len(polys))
        for polygon in polys:

            for point in polygon:
                _x = point[0]
                _y = point[1]

                if _x > points[0]['x'] and _y > points[0]['y']:
                    if _x > points[1]['x'] and _y < points[1]['y']:
                        if _x < points[2]['x'] and _y < points[2]['y']:
                            if _x < points[3]['x'] and _y > points[3]['y']:
                                pickedPoly = polys[idx] 

                # AM_vec = np.array([(point[1] - points[0]['x']), (point[0] - points[0]['y'])])
                # AM_dot_AB = np.dot(AM_vec, AB_vec)
                # # print(AB_dot_AB, AM_dot_AB, flush=True)

                # if not(AM_dot_AB < 0 or AM_dot_AB > AB_dot_AB):                
                #     score[idx] += 1
                # else:
                #     score[idx] -= 1

            idx += 1
            
        # print("score:", score, flush=True)
        # pickedPoly = polys[np.argmax(score)] 

        return [pickedPoly]      

    def getCoco(self, polys, category="unknow"):

        coco_image = im.Image(width=self.width, height=self.height)
        for i in range(len(polys)):
            
            mask = np.zeros((self.height, self.width))
            mask = cv2.fillPoly(mask, np.array([polys[i]]), 1)
            mask = im.Mask(mask)

            if mask.area() > self.min_area:
                class_name = 'unknown'
                category = im.Category(class_name)
                coco_image.add(mask, category=category)
            else:
                print("Area < thershold!! -> not included ")
        return {"coco": coco_image.coco()}
    
    def getPolys(self, mask):
        polys = im.Mask(mask).polygons()
        polyPoints = [
                np.array(point).reshape(-1, 2).round().astype(int)
                for point in polys
            ]
        return polyPoints
    
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
        # print(self.r, self.g, self.b, flush=True)
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

        return msk

model = vIndex()
