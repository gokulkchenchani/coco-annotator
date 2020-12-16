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

from ..util.vIndex import model as vIndex

api = Namespace('model', description='Model related operations')


image_upload = reqparse.RequestParser()
image_upload.add_argument('image', location='files', type=FileStorage, required=True, help='Image')

dextr_args = reqparse.RequestParser()
dextr_args.add_argument('points', location='json', type=list, required=True)
dextr_args.add_argument('padding', location='json', type=int, default=50)
dextr_args.add_argument('threshold', location='json', type=int, default=80)

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

# filter_args.add_argument('image', location='files', type=FileStorage, required=True, help='Image')

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


@api.route('/vindex/<int:image_id>')
class vindex(Resource):

    @login_required
    @api.expect(filter_args)
    
    def post(self, image_id):

        args = filter_args.parse_args()
        print(args, flush=True)

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

        coco = vIndex.getCoco(vIndex.predictMask(image,filter_type=filter_type,
                                        min_area=min_area,
                                        exg_threshold=exg_threshold,
                                        exgr_const=exgr_const,  
                                        exgr_threshold=exgr_threshold,
                                        cive_r=cive_r,
                                        cive_g=cive_g,
                                        cive_b=cive_b,
                                        cive_bias=cive_bias,
                                        cive_threshold=cive_threshold))
        return coco

@api.route('/vindex/fbox/<int:image_id>')
class vindex(Resource):

    @login_required
    @api.expect(filter_args)
    
    def post(self, image_id):

        print("Heree..... 1", flush=True)

        # args = filter_args.parse_args()

        print("Heree..... 11", flush=True)

        # print(args, flush=True)
        
        # image = Image.open(args.get('image'))

        # filter_type = args.get('filter_type')
        # min_area = args.get('min_area')
        # exg_threshold = args.get('exg_threshold')

        # exgr_const = args.get('exgr_const')
        # exgr_threshold = args.get('exgr_threshold')

        # cive_r = args.get('cive_r')
        # cive_g = args.get('cive_g')
        # cive_b = args.get('cive_b')
        # cive_bias = args.get('cive_bias')
        # cive_threshold = args.get('cive_threshold')


        # print("Heree..... 2", filter_type, min_area, exg_threshold, flush=True)


        image_model = ImageModel.objects(id=image_id).first()
        if not image_model:
            return {"message": "Invalid image ID"}, 400

        image = Image.open(image_model.path)
        polys = vIndex.getPolys(vIndex.predictMask(image))
        return 

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
