import numpy as np
import time
import cv2
import os
from gpiozero import Button
from translate import Translator
import speech_recognition as sr
from threading import Thread
from google_speech import Speech
import imutils
import subprocess
import pyttsx3
from gtts import gTTS 


def realtime_yolo_object_recognition():
    Thread(target=yolo_obj_voice_recog_stop).start()
    print("thread started")

    # load the COCO class labels our YOLO model was trained on
    LABELS = open("/home/pi/yolo/darknet/data/coco.names").read().strip().split("\n")

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet("/home/pi/yolo/darknet/cfg/yolov4-tiny.cfg", "/home/pi/yolo/darknet/weights/yolov4-tiny.weights")


    #yolo-coco/yolov3.cfg
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # initialize
    cap = cv2.VideoCapture(0)
    frame_count = 0
    start = time.time()
    first = True
    frames = []

    while True:
        
        with open('realtime_yolo_obj_recog_stop.txt', 'r') as r:
            lines = r.readlines()
        
        if "stop" in lines:
            
            file = open('realtime_yolo_obj_recog_stop.txt', 'r+')
            file.truncate(0)
            file.close()
            
            os.system('mpg321 yolo_stop_sound.mp3 &')
            
            break
        
        frame_count += 1
        # Capture frame-by-frameq
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        frames.append(frame)

        if ret:
            key = cv2.waitKey(1)
            if frame_count % 20 == 0:
                end = time.time()
                # grab the frame dimensions and convert it to a blob
                (H, W) = frame.shape[:2]
                # construct a blob from the input image and then perform a forward
                # pass of the YOLO object detector, giving us our bounding boxes and
                # associated probabilities
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                    swapRB=True, crop=False)
                net.setInput(blob)
                layerOutputs = net.forward(ln)

                # initialize our lists of detected bounding boxes, confidences, and
                # class IDs, respectively
                boxes = []
                confidences = []
                classIDs = []
                centers = []

                # loop over each of the layer outputs
                for output in layerOutputs:
                    # loop over each of the detections
                    for detection in output:
                        # extract the class ID and confidence (i.e., probability) of
                        # the current object detection
                        scores = detection[5:]
                        classID = np.argmax(scores)
                        confidence = scores[classID]

                        # filter out weak predictions by ensuring the detected
                        # probability is greater than the minimum probability
                        if confidence > 0.5:
                            # scale the bounding box coordinates back relative to the
                            # size of the image, keeping in mind that YOLO actually
                            # returns the center (x, y)-coordinates of the bounding
                            # box followed by the boxes' width and height
                            box = detection[0:4] * np.array([W, H, W, H])
                            (centerX, centerY, width, height) = box.astype("int")

                            # use the center (x, y)-coordinates to derive the top and
                            # and left corner of the bounding box
                            x = int(centerX - (width / 2))
                            y = int(centerY - (height / 2))

                            # update our list of bounding box coordinates, confidences,
                            # and class IDs
                            boxes.append([x, y, int(width), int(height)])
                            confidences.append(float(confidence))
                            classIDs.append(classID)
                            centers.append((centerX, centerY))

                # apply non-maxima suppression to suppress weak, overlapping bounding
                # boxes
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

                texts = []

                # ensure at least one detection exists
                if len(idxs) > 0:
                    # loop over the indexes we are keeping
                    for i in idxs.flatten():
                        # find positions
                        centerX, centerY = centers[i][0], centers[i][1]
                        
                        if centerX <= W/3:
                            W_pos = "left "
                        elif centerX <= (W/3 * 2):
                            W_pos = "center "
                        else:
                            W_pos = "right "
                        
                        if centerY <= H/3:
                            H_pos = "top "
                        elif centerY <= (H/3 * 2):
                            H_pos = "mid "
                        else:
                            H_pos = "bottom "

                        texts.append(H_pos + W_pos + LABELS[classIDs[i]])

                print(texts)
                
                if texts:
                    description = ', '.join(texts)
                    
                    # translate to bulgarian
                    #translator = Translator()
                    #translated = translator.translate(description, src='en', dest='bg')
                    
                    # create sound file in bulgarian
                    #tts = gTTS(translated, lang='bg')
                    
                    translator = Translator(to_lang="Bulgarian")
                    translation = translator.translate(description)
                    print(translation)
                    
                    translation = translation.replace('десен', 'дясно има ')
                    translation = translation.replace('ляв', 'ляво има ')
                    translation = translation.replace('долен', 'долу в ')
                    translation = translation.replace('долния', 'долу в ')
                    translation = translation.replace('горен', 'горе в ')
                    translation = translation.replace('горния', 'горе в ')
                    translation = translation.replace('средноцентров', 'в средата има ')
                    
                    
                    # create sound file in bulgarian
                    language = "bg"
                    speech = Speech(translation, language)
                    speech.save("yolo_objects.mp3")
                    os.system('mpg321 yolo_objects.mp3 &')

    cap.release()
    cv2.destroyAllWindows()


def stop_yolo_voice_recog():
    with open('realtime_yolo_obj_recog_stop.txt', 'w') as f:
        f.write('stop')
            

def yolo_obj_voice_recog_stop():
    r = sr.Recognizer()
    mic = sr.Microphone()
    stopBtn = Button(2)
    
    
    while True:
        
        stopBtn.when_pressed = stop_yolo_voice_recog
        
        try:
            
            with mic as source:
                audio = r.listen(source)
                
            text = r.recognize_google(audio)
            text = text.lower()
            
            print(f"Text: {text}")

            if "stop" in text:
                with open('realtime_yolo_obj_recog_stop.txt', 'w') as f:
                    f.write('stop')
                break

        except:
            pass


if __name__ == '__main__':
    realtime_yolo_object_recognition()