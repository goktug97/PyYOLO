#!/usr/bin/env python3

import cv2
from .cyolo import *
import numpy as np

class BBox(np.ndarray):
    def __new__(cls, x, y, w, h, prob, name):
        cls.name = name
        cls.prob = prob
        obj = np.asarray([x, y, w, h]).view(cls)
        obj.x, obj.y, obj.w, obj.h = obj.view()
        return obj

    def __str__(self):
        x, y, w, h = self.view()
        string = f'x: {x}, y: {y}, w: {w}, h: {h}, '
        string += f'probability: {self.prob}, name: {self.name}'
        return string

    def to_xyxy(self):
        x, y, w, h = self.view()
        return np.array([x, y, x + w, y + h])

    def __array_finalize__(self, obj):
        if obj is None: return


class YOLO(object):
    def __init__(self, config_path,
                 weights_path,
                 data_path,
                 detection_threshold = 0.5,
                 hier_threshold = 0.5,
                 nms_threshold = 0.5):

        if not os.path.exists(config_path):
            raise ValueError(f'Invalid config path: {os.path.abspath(config_path)}')
        if not os.path.exists(weights_path):
            raise ValueError(f'Invalid weight path: {os.path.abspath(weights_path)}')
        if not os.path.exists(data_path):
            raise ValueError(f'Invalid data file path: {os.path.abspath(data_path)}')

        self.net_main = load_net_custom(config_path.encode("ascii"),
                                        weights_path.encode("ascii"),
                                        0, 1)
        self.meta_main = load_meta(data_path.encode("ascii"))

        self.height = lib.network_height(self.net_main)
        self.width = lib.network_width(self.net_main)

        with open(data_path) as metaFH:
            meta_contents = metaFH.read()
            import re
            match = re.search("names *= *(.*)$",
                              meta_contents,
                              re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1)
            else:
                result = None
            if os.path.exists(result):
                with open(result) as namesFH:
                    names_list = namesFH.read().strip().split("\n")
                    self.alt_names = [x.strip() for x in names_list]

        self.threshold = detection_threshold
        self.hier_threshold = hier_threshold
        self.nms = nms_threshold


    def detect(self, image, rgb=False):
        original_h, original_w, _ = image.shape
        image = cv2.resize(image,
                           (self.width, self.height),
                           interpolation=cv2.INTER_CUBIC)[:,:,::-1]
        if not rgb:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im, arr = array_to_image(image)

        num = c_int(0)
        pnum = pointer(num)

        predict_image(self.net_main, im)
        dets = get_network_boxes(
            self.net_main, im.w, im.h,
            self.threshold,
            self.hier_threshold,
            None, 0, pnum, 0)
        num = pnum[0]

        if self.nms:
            do_nms_sort(dets, num, self.meta_main.classes, self.nms)

        res = []
        for j in range(num):
            for i in range(self.meta_main.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox

                    # coordinates as percentage
                    x = (b.x-b.w/2)/self.width
                    y = (b.y-b.h/2)/self.height
                    w = b.w/self.width
                    h = b.h/self.height

                    # scale detections to input image
                    x = int(round(x*original_w))
                    y = int(round(y*original_h))
                    w = int(round(w*original_w))
                    h = int(round(h*original_h))

                    bbox = BBox(x, y, w, h, dets[j].prob[i], self.alt_names[i])

                    res.append(bbox)

        free_detections(dets, num)
        return res

    
