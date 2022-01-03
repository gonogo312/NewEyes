import numpy as np
import sys
import os
import imutils

from yolo import Yolo
import cv2
from gtts import gTTS
import time


yolo = Yolo(confidence_param=0.3, thresh_param=0.5)


def yolo_object_detection_image():
    img = cv2.imread('/home/pi/Desktop/output-1.jpg')

    print("recognizing objects...")
    detection = yolo.detect(img)

    bounding_image = yolo.draw_results(
        detection, img)

    os.system('mpg321 yolo_objects.mp3 &')
        
    # optional lines of code
    
    #cv2.imshow('image', bounding_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    

def yolo_object_detection_stream():
    vs = cv2.VideoCapture(0)
    writer = None
    (W, H) = (None, None)
    
    while True:
        # read the next frame from the file
        (grabbed, frame) = vs.read()
     
        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]
            
        detection = yolo.detect(frame)

        bounding_image = yolo.draw_results(
            detection, frame)
        
        
        #os.system('mpg321 yolo_objects.mp3 &')
        
        # Optional lines of code
        time.sleep(2)
        
    
if __name__ == "__main__":
    print("Starting Yolo ...")
    yolo_object_detection_image()