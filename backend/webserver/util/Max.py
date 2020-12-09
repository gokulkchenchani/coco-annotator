

import numpy as np                                 # (pip install numpy)
from skimage import measure                        # (pip install scikit-image)
from shapely.geometry import Polygon, MultiPolygon # (pip install Shapely)
from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image , ImageFilter , ImageDraw 
import numpy as np
import logging
import cv2

class Max():

    def create_sub_mask_annotation(self, image, image_id=0, category_id = 0, is_crowd=False):
        image = image.convert('RGB')
        width, height = image.size
        # print(image.getbands(), flush=True)
        r, g, b = image.split()
        exg = 2 * np.array(g).astype('int32') -  np.array(b).astype('int32') - np.array(r).astype('int32')
        exg[exg < 30]  = 0
        exg[exg > 30] = 255
        exg = exg.astype('uint8')
        img = Image.fromarray(exg)
        polys = im.Mask(img).polygons()
        points = [
                np.array(point).reshape(-1, 2).round().astype(int)
                for point in polys
            ]
        print(len(points), type(points), type(points[0]), flush=True)
        coco_image = im.Image(width=width, height=height)
        for i in range(len(points)):
            mask = np.zeros((height, width))
            mask = cv2.fillPoly(mask, np.array([points[i]]), 1)
            mask = im.Mask(mask)
            if mask.area() > 100:
                class_id = i
                class_name = 'crop'
                category = im.Category(class_name)
                coco_image.add(mask, category=category)

        return coco_image.coco()

        # masks = [
        #         im.Mask(poly)
        #         for poly in polys
        #     ]
        # i = 0
        # for mask in masks:
        #     coco_image = im.Image(width=width, height=height)
        #     class_id = i
        #     class_name = 'crop'
        #     category = im.Category(class_name)
        #     coco_image.add(mask, category=category)
        #     i = i + 1
        # return coco_image.coco()

model = Max()
