# AgRobot COCO-Annotator

Bonn Agricultural Robotics Annotation tool forked from [jsbroks' COCO-Annotator](https://github.com/jsbroks/coco-annotator).

This adds multiple features to make agrigultural related annotation easier.

# AgRobot-COCO-Annotator additional features

- Most common agricultural related image filters (**ExG**, **ExGExR**, **CIVE**)
- PyTorch support
- Run PyTorch Mask-RCNN on images to produce annotations
- Cofigurable auto-backup of the annotation database and simple recovery tools
- Default high resolution annotation polygons

# COCO-Annotator original features

- Directly export to COCO format
- Segmentation of objects
- Ability to add key points
- Useful API endpoints to analyze data
- Import datasets already annotated in COCO format
- Annotate disconnect objects as a single instance
- Labeling image segments with any number of labels simultaneously
- Allow custom metadata for each instance or object
- Advanced selection tools such as, [DEXTR](https://github.com/jsbroks/dextr-keras), [MaskRCNN](https://github.com/matterport/Mask_RCNN) and Magic Wand
- Annotate images with semi-trained models
- Generate datasets using google images
- User authentication system

For examples and more information check out the [wiki](https://github.com/jsbroks/coco-annotator/wiki).


# More info in the original repo:

<p align="center"><img src="https://i.imgur.com/AA7IdbQ.png"></p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="https://github.com/jsbroks/coco-annotator/wiki">Wiki</a> •
  <a href="https://github.com/jsbroks/coco-annotator/wiki/Getting-Started">Getting Started</a> •
  <a href="https://github.com/jsbroks/coco-annotator/issues">Issues</a> •
  <a href="#license">License</a>
</p>

---

COCO Annotator is a web-based image annotation tool designed for versatility and efficiently label images to create training data for image localization and object detection. It provides many distinct features including the ability to label an image segment (or part of a segment), track object instances, labeling objects with disconnected visible parts, efficiently storing and export annotations in the well-known [COCO format](http://cocodataset.org/#format-data). The annotation process is delivered through an intuitive and customizable interface and provides many tools for creating accurate datasets.


<br />

<p align="center"><a href="http://www.youtube.com/watch?feature=player_embedded&v=OMJRcjnMMok" target="_blank"><img src="https://img.youtube.com/vi/OMJRcjnMMok/maxresdefault.jpg"
alt="Image annotations using COCO Annotator" width="600" /></a></p>
<p align="center"><i>Checkout the video for a basic guide on installing and using COCO Annotator.</i></p>

<br />

<p align="center"><img width="600" src="https://i.imgur.com/m4RmjCp.gif"></p>
<p align="center"><i>Note: This video is from v0.1.0 and many new features have been added.</i></p>


# Built With

Thanks to all these wonderful libaries/frameworks:

### Backend

- [Flask](http://flask.pocoo.org/) - Python web microframework
- [MongoDB](https://www.mongodb.com/) - Cross-platform document-oriented database
- [MongoEngine](http://mongoengine.org/) - Python object data mapper for MongoDB

### Frontend

- [Vue](https://vuejs.org/) - JavaScript framework for building user interfaces
- [Axios](https://github.com/axios/axios) - Promise based HTTP client
- [PaperJS](http://paperjs.org/) - HTML canvas vector graphics library
- [Bootstrap](https://getbootstrap.com/) - Frontend component library

# License

[MIT](https://tldrlegal.com/license/mit-license)

# Citation

```
  @MISC{cocoannotator,
    author = {Justin Brooks},
    title = {{COCO Annotator}},
    howpublished = "\url{https://github.com/jsbroks/coco-annotator/}",
    year = {2019},
  }
```
