from config import Config as AnnotatorConfig
from skimage.transform import resize
import imantics as im

import torch

from agrobot_mrcnn.models import MaskrcnnSweetPepperProtected

import logging
logger = logging.getLogger('gunicorn.error')


CUDA_DEVICE_NUM = AnnotatorConfig.CUDA_DEVICE_NUM

MODEL_DIR = "/workspace/models"
MODEL_PATH = AnnotatorConfig.TORCH_MASK_RCNN_FILE
CLASS_NAMES = AnnotatorConfig.TORCH_MASK_RCNN_CLASSES.split(',')



class TorchMaskRCNN():

    def __init__(self):

        self.device = 'cpu'
        # try finding the specified CUDA device, use cpu otherwise
        if CUDA_DEVICE_NUM:
            try:
                assert torch.cuda.is_available()
                assert int(CUDA_DEVICE_NUM) < torch.cuda.device_count()
                self.device = torch.device(f'cuda:{int(CUDA_DEVICE_NUM)}')
                logger.info(f"[Torch] Using CUDA device ({CUDA_DEVICE_NUM})")
            except:
                logger.info(f"[Torch] Unable find CUDA device ({CUDA_DEVICE_NUM}), using cpu instead")
        try:
            self.model = MaskrcnnSweetPepperProtected()
            self.model.load_state_dict(torch.load(MODEL_PATH))
            logger.info(f"[Torch] instanciated Torch MaskRCNN model: {MODEL_PATH}")
            self.model.to(self.device)
            logger.debug(f"[Torch] Sent model to device")
        except:
            logger.error(f"[Torch] Unable to initialize Torch model")
            self.model = None


    def detect(self, image):

        if self.model is None:
            return {}

        logger.info(f"[Torch placeholders] Image preprocesing")

        logger.info(f"[Torch placeholders] Detecting instances")

        logger.info(f"[Torch placeholders] convert to coco format")

        width, height = image.size
        return im.Image(width=width, height=height).coco()


model = TorchMaskRCNN()
