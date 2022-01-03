from google_speech import Speech
from image_processing import *
from gpiozero import Button
from gtts import gTTS
import random
import cv2
from PIL import Image
import os
import easyocr

def get_grayscale(image):
    images = np.array(Image.open(image))

    gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    return gray

def text_recognition():
    
    os.system("pkill mpg321")

    language = ''
    os.environ['OMP_THREAD_LIMIT'] = '1'
    IMAGE_PATH = "/home/pi/Desktop/stop.jpeg"
    os.system("mpg321 /home/pi/please_wait.mp3 &")



    print("pre-processing...")
    
    gray = get_grayscale(IMAGE_PATH)
    cv2.imwrite('/home/pi/grayscale.jpg', gray)
    
    print("pre-processing finished...")
    
    
    
    osd = pytesseract.image_to_osd('/home/pi/grayscale.jpg', config='--psm 0 -c min_characters_to_try=3')
    print(osd)

        
    if "Script: Cyrillic" in osd:
        language = 'bg'
    elif "Script: Latin" in osd:
        language = 'en'
    else:
        language = 'en'
    # Dewarp code goes here...
    
    reader = easyocr.Reader([language])
    result = reader.readtext(IMAGE_PATH)
    print(result)
        
    #gtts_speak(str(text), language)
    

def kill_mpg():
    os.system("pkill mpg321")
    
    
def gtts_speak(text, language):
    if text != "":
        speech = Speech(text, language)
        speech.save("page.mp3")
        os.system('mpg321 page.mp3 &')

    else:
        errorMessages = ["ocr_error_1.mp3",
                         "ocr_error_2.mp3",
                         "ocr_error_3.mp3"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        os.system('mpg321 ' + '/home/pi/error_messages/' + chosen_message + ' &')

text_recognition()


