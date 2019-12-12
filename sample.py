import cv2
import pyyolo

def main():
    detector = pyyolo.YOLO("/home/goktug/libraries/retracker/models/yolov3-spp.cfg",
                           "/home/goktug/libraries/retracker/models/yolov3-spp.weights",
                           "/home/goktug/libraries/retracker/models/coco.data",
                           detection_threshold = 0.5,
                           hier_threshold = 0.5,
                           nms_threshold = 0.45)

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        dets = detector.detect(frame)
        for det in dets:
            xmin, ymin, xmax, ymax = det.to_xyxy()
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255))
        cv2.imshow('cvwindow', frame)
        if cv2.waitKey(1) == 27:
            break

if __name__ == '__main__':
    main()
