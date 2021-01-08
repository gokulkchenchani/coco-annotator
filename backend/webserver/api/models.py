from flask_restplus import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from imantics import Mask
from flask_login import login_required
from config import Config
from PIL import Image
from database import ImageModel

import imantics as im

import os
import math
import logging

logger = logging.getLogger('gunicorn.error')


MASKRCNN_LOADED = os.path.isfile(Config.MASK_RCNN_FILE)
if MASKRCNN_LOADED:
    from ..util.mask_rcnn import model as maskrcnn
else:
    logger.warning("MaskRCNN model is disabled.")

TORCHMASKRCNN_LOADED = os.path.isfile(Config.TORCH_MASK_RCNN_FILE)
if TORCHMASKRCNN_LOADED:
    from ..util.torch_mask_rcnn import model as torch_maskrcnn
else:
    logger.warning("Torch MaskRCNN model is disabled.")

DEXTR_LOADED = os.path.isfile(Config.DEXTR_FILE)
if DEXTR_LOADED:
    from ..util.dextr import model as dextr
else:
    logger.warning("DEXTR model is disabled.")

from ..util.vIndex import model as vIndex

api = Namespace('model', description='Model related operations')


image_upload = reqparse.RequestParser()
image_upload.add_argument('image', location='files', type=FileStorage, required=True, help='Image')

dextr_args = reqparse.RequestParser()
dextr_args.add_argument('points', location='json', type=list, required=True)
dextr_args.add_argument('padding', location='json', type=int, default=50)
dextr_args.add_argument('threshold', location='json', type=int, default=80)





# filter_args.add_argument('image', location='files', type=FileStorage, required=True, help='Image')

@api.route('/dextr/<int:image_id>')
class Dextr(Resource):

    @login_required
    @api.expect(dextr_args)

    def post(self, image_id):
        """ COCO data test """

        if not DEXTR_LOADED:
            return {"disabled": True, "message": "DEXTR is disabled"}, 400

        args = dextr_args.parse_args()
        points = args.get('points')
        # padding = args.get('padding')
        # threshold = args.get('threshold')

        if len(points) != 4:
            return {"message": "Invalid points entered"}, 400

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        result = dextr.predict_mask(image, points)

        return { "segmentaiton": Mask(result).polygons().segmentation }


@api.route('/maskrcnn')
class MaskRCNN(Resource):

    @login_required
    @api.expect(image_upload)
    def post(self):
        """ COCO data test """
        if not MASKRCNN_LOADED:
            return {"disabled": True, "coco": {}}

        args = image_upload.parse_args()
        im = Image.open(args.get('image'))
        coco = maskrcnn.detect(im)
        return coco

filter_args = reqparse.RequestParser()
filter_args.add_argument('min_area', location='json', type=int, default=50)
filter_args.add_argument('filter_type', location='json', type=int, required=True)

filter_args.add_argument('exg_padding', location='json', type=int, default=50)
filter_args.add_argument('exg_threshold', location='json', type=int, default=30)

filter_args.add_argument('exgr_const', location='json', type=float, default=1.4)
filter_args.add_argument('exgr_threshold', location='json', type=int, default=30)

filter_args.add_argument('cive_r', location='json', type=float, default=0.441)
filter_args.add_argument('cive_g', location='json', type=float, default=0.811)
filter_args.add_argument('cive_b', location='json', type=float, default=0.385)
filter_args.add_argument('cive_bias', location='json', type=float, default=18.78745)
filter_args.add_argument('cive_threshold', location='json', type=int, default=10)

@api.route('/vindex/<int:image_id>')
class vindex(Resource):

    @login_required
    @api.expect(filter_args)

    def post(self, image_id):

        args = filter_args.parse_args()
        # print(args, flush=True)

        filter_type = args.get('filter_type')
        min_area = args.get('min_area')
        exg_threshold = args.get('exg_threshold')

        exgr_const = args.get('exgr_const')
        exgr_threshold = args.get('exgr_threshold')

        cive_r = args.get('cive_r')
        cive_g = args.get('cive_g')
        cive_b = args.get('cive_b')
        cive_bias = args.get('cive_bias')
        cive_threshold = args.get('cive_threshold')

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        mask = vIndex.predictMask(image,filter_type=filter_type,
                                        min_area=min_area,
                                        exg_threshold=exg_threshold,
                                        exgr_const=exgr_const,
                                        exgr_threshold=exgr_threshold,
                                        cive_r=cive_r,
                                        cive_g=cive_g,
                                        cive_b=cive_b,
                                        cive_bias=cive_bias,
                                        cive_threshold=cive_threshold)
        coco = vIndex.getCoco(vIndex.getPolys(mask))
        return coco


fbox_args = reqparse.RequestParser()
fbox_args.add_argument('points', location='json',type=list, required=True)
fbox_args.add_argument('min_area', location='json', type=int, default=50)
fbox_args.add_argument('filter_type', location='json', type=int, required=True)

fbox_args.add_argument('exg_padding', location='json', type=int, default=50)
fbox_args.add_argument('exg_threshold', location='json', type=int, default=30)

fbox_args.add_argument('exgr_const', location='json', type=float, default=1.4)
fbox_args.add_argument('exgr_threshold', location='json', type=int, default=30)

fbox_args.add_argument('cive_r', location='json', type=float, default=0.441)
fbox_args.add_argument('cive_g', location='json', type=float, default=0.811)
fbox_args.add_argument('cive_b', location='json', type=float, default=0.385)
fbox_args.add_argument('cive_bias', location='json', type=float, default=18.78745)
fbox_args.add_argument('cive_threshold', location='json', type=int, default=10)


@api.route('/fbox/<int:image_id>')
class fbox(Resource):

    @login_required
    @api.expect(fbox_args)

    def post(self, image_id):

        args = fbox_args.parse_args()
        # print(args.get('points'), flush=True)

        points = args.get('points')
        filter_type = args.get('filter_type')
        min_area = args.get('min_area')
        exg_threshold = args.get('exg_threshold')

        exgr_const = args.get('exgr_const')
        exgr_threshold = args.get('exgr_threshold')

        cive_r = args.get('cive_r')
        cive_g = args.get('cive_g')
        cive_b = args.get('cive_b')
        cive_bias = args.get('cive_bias')
        cive_threshold = args.get('cive_threshold')

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        mask = vIndex.predictMask(image,filter_type=filter_type,
                                        min_area=min_area,
                                        exg_threshold=exg_threshold,
                                        exgr_const=exgr_const,
                                        exgr_threshold=exgr_threshold,
                                        cive_r=cive_r,
                                        cive_g=cive_g,
                                        cive_b=cive_b,
                                        cive_bias=cive_bias,
                                        cive_threshold=cive_threshold)
        pickedPoly = vIndex.pickPoly(mask, points)
        coco = vIndex.getCoco(pickedPoly)
        return coco


torchbox_args = reqparse.RequestParser()
torchbox_args.add_argument('points', location='json',type=list, required=True)

@api.route('/torchbox/<int:image_id>')
class torchbox(Resource):

    @login_required
    @api.expect(torchbox_args)

    def post(self, image_id):
        if not TORCHMASKRCNN_LOADED:
            logger.warning("No torch_mrcnn model loaded.")
            return {"disabled": True, "coco": {}}

        args = torchbox_args.parse_args()
        # image centered coordinate system
        points = args.get('points')

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        width, height = image.size
        image = image.convert('RGB')

        # Detection box coordinates to extreme pixels
        b_xs = [max(min(p['x'] + width/2, width), 0) for p in points]
        b_ys = [max(min(p['y'] + height/2, height), 0) for p in points]
        crop_box = (math.ceil(min(b_xs)),   # left limit
                    math.ceil(min(b_ys)),   # top limit
                    math.floor(max(b_xs)),   # right limit
                    math.floor(max(b_ys)))   # bottom limit

        # Entered box outside of the image canvas
        if crop_box[0] == crop_box[2] or crop_box[1] == crop_box[3]:
            logger.warning("Invaid box for detection given.")
            return im.Image(width=0, height=0).coco()

        coco = torch_maskrcnn.detect_in_box(image, crop_box)
        return {"coco": coco}
        # coco = {"coco": None}
        # return coco

@api.route('/torch_maskrcnn')
class TorchMaskRCNN(Resource):

    @login_required
    @api.expect(image_upload)
    def post(self):
        """ COCO data test """
        if not TORCHMASKRCNN_LOADED:
            logger.warning("No torch_mrcnn model loaded.")
            return {"disabled": True, "coco": {}}

        args = image_upload.parse_args()
        im = Image.open(args.get('image'))
        coco = torch_maskrcnn.detect(im)
        return {"coco": coco}
