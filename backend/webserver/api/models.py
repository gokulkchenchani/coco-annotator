from flask_restplus import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from imantics import Mask
from flask_login import login_required
from config import Config
from PIL import Image
from database import ImageModel

import os
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

from ..util.exg import model as exgIndex
from ..util.exgexr import model as exgexrIndex
from ..util.cive import model as civeIndex

api = Namespace('model', description='Model related operations')


image_upload = reqparse.RequestParser()
image_upload.add_argument('image', location='files', type=FileStorage, required=True, help='Image')

dextr_args = reqparse.RequestParser()
dextr_args.add_argument('points', location='json', type=list, required=True)
dextr_args.add_argument('padding', location='json', type=int, default=50)
dextr_args.add_argument('threshold', location='json', type=int, default=80)

exg_args = reqparse.RequestParser()
exg_args.add_argument('exg_padding', location='json', type=int, default=50)
exg_args.add_argument('exg_threshold', location='json', type=int, default=30)

exgexr_args = reqparse.RequestParser()
exgexr_args.add_argument('exgexr_const', location='json', type=float, default=1.4)
exgexr_args.add_argument('exgexr_threshold', location='json', type=int, default=30)

cive_args = reqparse.RequestParser()
cive_args.add_argument('cive_r', location='json', type=float, default=0.441)
cive_args.add_argument('cive_g', location='json', type=float, default=0.811)
cive_args.add_argument('cive_b', location='json', type=float, default=0.385)
cive_args.add_argument('cive_bias', location='json', type=float, default=18.78745)
cive_args.add_argument('cive_threshold', location='json', type=int, default=30)

@api.route('/dextr/<int:image_id>')
class MaskRCNN(Resource):

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
        return {"coco": coco}


@api.route('/exg/<int:image_id>')
class ExG(Resource):

    @login_required
    @api.expect(exg_args)

    def post(self, image_id):

        args = exg_args.parse_args()

        padding = args.get('exg_padding')
        threshold = args.get('exg_threshold')

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        result = exgIndex.predictMask(image, padding=padding, threshold=threshold)

        return { "segmentaiton": Mask(result).polygons().segmentation }

@api.route('/exgexr/<int:image_id>')
class ExGExR(Resource):

    @login_required
    @api.expect(exgexr_args)
    def post(self, image_id):

        args = exgexr_args.parse_args()

        const = args.get('exgexr_const')
        threshold = args.get('exgexr_threshold')

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        result = exgexrIndex.predictMask(image, const=const, threshold=threshold)

        return { "segmentaiton": Mask(result).polygons().segmentation }

@api.route('/cive/<int:image_id>')
class CIVE(Resource):

    @login_required
    @api.expect(cive_args)
    def post(self, image_id):

        args = cive_args.parse_args()

        cive_r = args.get('cive_r')
        cive_g = args.get('cive_g')
        cive_b = args.get('cive_b')
        cive_bias = args.get('cive_bias')
        threshold = args.get('cive_threshold')

        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        result = civeIndex.predictMask(image, 
                                        cive_r=cive_r,
                                        cive_g=cive_g,
                                        cive_b=cive_b,
                                        cive_bias=cive_bias,
                                        threshold=threshold)

        return { "segmentaiton": Mask(result).polygons().segmentation }


@api.route('/torch_maskrcnn')
class MaskRCNN(Resource):

    @login_required
    @api.expect(image_upload)
    def post(self):
        """ COCO data test """
        if not TORCHMASKRCNN_LOADED:
            return {"disabled": True, "coco": {}}

        args = image_upload.parse_args()
        im = Image.open(args.get('image'))
        coco = torch_maskrcnn.detect(im)
        return {"coco": coco}
