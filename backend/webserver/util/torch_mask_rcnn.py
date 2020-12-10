from config import Config as AnnotatorConfig
import imantics as im

import torch
import torchvision.transforms as transforms
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
            self.model.eval()
            logger.info(f"[Torch] instanciated Torch MaskRCNN model: {MODEL_PATH}")
            self.model.to(self.device)
            logger.debug(f"[Torch] Sent model to device")
        except:
            logger.error(f"[Torch] Unable to initialize Torch model")
            self.model = None

    @torch.no_grad()
    def detect(self, image):

        if self.model is None:
            return {}

        logger.info(f"[Torch] Image preprocesing")
        width, height = image.size
        image = image.convert('RGB')
        # Send image to compute device
        image = transforms.ToTensor()(image).to(self.device)
        torch.cuda.synchronize()

        logger.info(f"[Torch] Detecting instances")
        outputs = self.model([image])
        # Put results in cpu and get masks and labels
        outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]
        masks = torch.squeeze(outputs[0]['masks'])
        class_ids = torch.squeeze(outputs[0]['labels'])

        logger.info(f"[Torch] convert to coco format")
        coco_image = im.Image(width=width, height=height)
        for i in range(masks.shape[0]):
            binary_mask = masks[i].numpy()
            binary_mask[binary_mask < 0.9] = 0.
            mask = im.Mask(binary_mask)
            class_name = 'pepper'
            category = im.Category(CLASS_NAMES[class_ids[i]])
            coco_image.add(mask, category=category)

        return coco_image.coco()


model = TorchMaskRCNN()
