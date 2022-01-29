import cv2
import numpy as np
from pyzbar.pyzbar import decode
from tldextract import extract
from gpiozero import Button
import multiprocessing
from gtts import gTTS
from pygame import mixer
import pyttsx3
import RPi.GPIO as GPIO  
from threading import Thread
import time
from textblob import TextBlob
from langdetect import detect
import os


def gtts_speak(text):
    
    if text != "":
        #tts = gTTS(text, lang=var)
        #print(detect(text))
        #language = detect(text)
        engine = pyttsx3.init()
        
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 110)
        
        engine.say(text)
        engine.runAndWait()
        


def domain_extractor(urlName):
    tsd, td, tsu = extract(urlName)  # prints abc, hostname, com
    url = td + '.' + tsu  # will prints as hostname.com
    return url


btnFlag = 0
def stop_qr_barcode_detection(self):
    print("Stopping qr and barcode detection...")
    global btnFlag
    btnFlag += 1
    

def stop_button_thread():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 3 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(3,GPIO.RISING,callback=stop_qr_barcode_detection) # Setup event on pin 3 rising edge
    
    
def start_qr_barcode_recognition():
    Thread(target=stop_button_thread, daemon=True).start()
    
    global btnFlag
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
    
        data = domain_extractor(data)
        
        if len(data) < 5:
            data = ""
        
        if data:
            
            mixer.init()
            mixer.music.load("qr_detected.mp3")
            mixer.music.set_volume(0.7)
            mixer.music.play()
    
            time.sleep(2)

            print("data found: ", data)
            gtts_speak(data)
            time.sleep(1.7)
            
        cv2.imshow("code detector", img)
        
        code = cv2.waitKey(10)
        
        if btnFlag == 1:
            cap.release()
            cv2.destroyAllWindows()
            break
    
        
if __name__ == "__main__":
    start_qr_barcode_recognition()
    