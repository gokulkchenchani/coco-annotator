from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im
from PIL import Image
import numpy as np
import logging
logger = logging.getLogger('gunicorn.error')

# class FilterRunConfig(Config):
#     """
#     Configuration for COCO Dataset.
#     """
#     NAME = "coco"
#     GPU_COUNT = 1
#     IMAGES_PER_GPU = 1
#     NUM_CLASSES = len(CLASS_NAMES)

def ExgIndex(image):
    return (2 * image[1] - image[:,0] - image[:,2])
class ExG():

    def __init__(self):
        print("ExG initialized!!")
        # self.config = FilterRunConfig()


    def predict_mask(self, image):

        image = image.convert('RGB')
        width, height = image.size
        image.thumbnail((1024, 1024))
        # ExgIndexVecfunc = np.vectorize(ExgIndex)
        result = np.zeros((width, height))
        result[:, 1:height] = 1
        print(image.size)
        masks = result.get('masks')
        class_ids = result.get('class_ids')

        coco_image = im.Image(width=width, height=height)

        for i in range(masks.shape[-1]):
            mask = resize(masks[..., i], (height, width))
            mask = im.Mask(mask)
            class_id = class_ids[i]
            class_name = CLASS_NAMES[class_id]
            category = im.Category(class_name)
            coco_image.add(mask, category=category)

        return coco_image.coco()


model = ExG()
