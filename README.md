# AgRobot COCO-Annotator

Bonn Agricultural Robotics Annotation tool forked from [jsbroks' COCO-Annotator](https://github.com/jsbroks/coco-annotator).

This adds multiple features to make agricultural related annotation easier.

## AgRobot-COCO-Annotator additional features

- Most common agricultural related image filters (**ExG**, **ExGExR**, **CIVE**)
- PyTorch support
- Run PyTorch Mask-RCNN on images to produce annotations
- Configurable auto-backup of the annotation database and simple recovery tools
- Default high resolution annotation polygons

## COCO-Annotator original features

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

## Install & Run server with PyTorch and CUDA support
In order to run PyTorch models on GPU, `nvidia docker runitime utilities` must be installed and configured on the server machine before running the annotation server.

### Run install script
```[path_to_repo]/scripts/install.sh```

This script will:
- Install `nvidia docker runitime utilities`
- Build a `python3` environment with `torch` and `cuDNN` support as a `docker` container
- Generate deploy keys and save them in `/scripts/keys`, which [need to be added](https://docs.github.com/en/free-pro-team@latest/developers/overview/managing-deploy-keys) to any repositories you want to use (for now only `Agricultural-Robotics-Bonn/agrobot-pytorch-mask-rcnn`)

### Run server with PyTorch and CUDA support
After installing and adding the depoly `ssh-key` to your repos, run the server with the following commands:

```
cd [path_to_annotator_repo]
sudo docker-compose -f docker-compose.torch_build.yml up --build
```

## Database Auto-Backup configuration and recovery

Database auto-backup only works if the servers database is running a replica set.

The replica set and backup scheme are configured in the server's `docker-compose` file.

Files supporting this are:
- **`docker-compose.build.yml`**
- **`docker-compose.torch_build.yml`**.

### Auto-Backup configuration
To change the auto-backup settings, edit the `backup` service entry on the `docker-compose` file you intend to run.

The most relevant settings you can change are:
- Backup path:

```
  volumes:
    - [server_backup_path_here]:/backup
```

- Backup frequency (in [crontab format](https://crontab.guru/))

```
  environment:
    - CRON_TIME=[crontab_backup_frequency_here]
```

### Database Backup recovery
List the names of available backup files:

```ls [server_backup_path_here]```

With the annotation server running, run the following command on the server machine to restore the derired backup:

``` docker exec annotator_backup /restore.sh /backup/database-[backup_timestamp].archive.gz ```

## TODOs:
- Automate `Agrobot-MaskRCNN` download when building docker images. 
- Remove bbox used by box based detectors from instance list (e.g.: `torchbox`)
- `Agrobot-MaskRCNN` has poor performance when used with `torchbox` in small bounding boxes.
- Increase DEXTR detection mask's resolution (if possible)
- Fix: After images stay open for a long time, the annotator becomes slow and crashes. When that image is re-opened, all instance masks are missing but are still listed on the right pannel. If the image gets saved, all annotations for that Image get lost.

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
