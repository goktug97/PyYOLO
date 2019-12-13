Python Wrapper for the YOLO
===================================


### Installation


#### Dependencies
- Linux
- Python >= 3.6
- [Darknet Shared Library](https://github.com/AlexeyAB/darknet#how-to-use-yolo-as-dll-and-so-libraries)
- numpy
- OpenCV

#### Darknet Shared Library
You should first install [darknet](https://github.com/AlexeyAB/darknet "darknet")
library with `BUILD_SHARED_LIBS` set to ON.
After the installation the LIB_DARKNET environment variable should be set to
shared library path. The path is required in runtime so my recommendation is 
adding this to your rc file. `export LIB_DARKNET=<path_to_libdarknet.so>`

#### PyYOLO

##### From PyPi
``` shell
pip3 install pyyolo --user
```

##### From source
``` shell
git clone https://github.com/goktug97/PyYOLO
cd PyYOLO
python3 setup.py install --user
```

### Documentation

#### Example

`python sample.py`

[sample.py](https://github.com/goktug97/PyYOLO/blob/master/sample.py)

``` python
import cv2
import pyyolo

def main():
    detector = pyyolo.YOLO("./models/yolov3-spp.cfg",
                           "./models/yolov3-spp.weights",
                           "./models/coco.data",
                           detection_threshold = 0.5,
                           hier_threshold = 0.5,
                           nms_threshold = 0.45)

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        dets = detector.detect(frame, rgb=False)
        for i, det in enumerate(dets):
            print(f'Detection: {i}, {det}')
            xmin, ymin, xmax, ymax = det.to_xyxy()
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255))
        cv2.imshow('cvwindow', frame)
        if cv2.waitKey(1) == 27:
            break

if __name__ == '__main__':
    main()
```

#### BBox Class
This class is just a numpy array with extra attributes and functions.

``` python-console
Python 3.8.0 (default, Oct 23 2019, 18:51:26)
[GCC 9.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyyolo
>>> bbox = pyyolo.BBox(x=10, y=20, w=100, h=200, prob=0.9, name='person')
>>> bbox
BBox([ 10,  20, 100, 200])
>>> print(bbox)
x: 10, y: 20, w: 100, h: 200, probability: 0.9, name: person
>>> x, y, w, h = bbox
>>> print(x, y, w, h)
10 20 100 200
>>> bbox + bbox
BBox([ 20,  40, 200, 400])
>>> bbox.prob
0.9
>>> bbox.name
'person'
>>> xmin, ymin, xmax, ymax = bbox.to_xyxy()
>>> xmin, ymin, xmax, ymax
(10, 20, 110, 220)
```

#### YOLO Class
- detect function returns list of BBox Instances. See [sample.py](https://github.com/goktug97/PyYOLO/blob/master/sample.py) for example usage.

### License
PyYOLO is licensed under the MIT License.
