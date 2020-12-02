from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im

from keras.preprocessing.image import img_to_array
from mrcnn.config import Config
import mrcnn.model as modellib
import logging
logger = logging.getLogger('gunicorn.error')


MODEL_DIR = "/workspace/models"
COCO_MODEL_PATH = AnnotatorConfig.TORCH_MASK_RCNN_FILE
CLASS_NAMES = AnnotatorConfig.TORCH_MASK_RCNN_CLASSES.split(',')



class TorchMaskRCNN():

    def __init__(self):

        logger.info(f"[Torch placeholders] Instanciating Torch MaskRCNN model: {COCO_MODEL_PATH}")
        self.model = [0]

        logger.info(f"[Torch placeholders] Try to load model")


    def detect(self, image):

        if self.model is None:
            return {}

        logger.info(f"[Torch placeholders] Image preprocesing")

        logger.info(f"[Torch placeholders] Detecting instances")

        logger.info(f"[Torch placeholders] convert to coco format")

        width, height = image.size
        return im.Image(width=width, height=height).coco()


model = TorchMaskRCNN()
