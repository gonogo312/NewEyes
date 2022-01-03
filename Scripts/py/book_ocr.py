from google_speech import Speech
from image_processing import *
from gpiozero import Button
from gtts import gTTS
import random
import os


def text_recognition():
    
    os.system("pkill mpg321")

    language = ''
    os.environ['OMP_THREAD_LIMIT'] = '1'
    IMAGE_PATH = "/home/pi/Desktop/elonmusk.jpg"
    os.system("mpg321 /home/pi/please_wait.mp3 &")

    
    print("pre-processing...")
    # Deskew the given image after the
    # Preprocessing stage is done
    modified_img = process_image(IMAGE_PATH)
    deskew('/home/pi/processed_image.jpg')
    
    print("pre-processing finished...")
    # Check the processed image for
    # Any text that is upside down
    
    osd = ''
    try:
        osd = pytesseract.image_to_osd('/home/pi/deskewed_image.jpg', config='--psm 0 -c min_characters_to_try=10')
        print(osd)
    except:
        pass
        
    if "Script: Cyrillic" in osd:
        language = 'bul'
    elif "Script: Latin" in osd:
        language = 'eng'
    else:
        language = 'eng'
    # Dewarp code goes here...
    
    text = ''
    # Flip the image case
    if "Orientation in degrees: 180" in osd:
        im = Image.open('/home/pi/deskewed_image.jpg')
        angle = 180
        out = im.rotate(angle)
        out.save("/home/pi/flipped_image.jpg")
        text = text_extraction('/home/pi/flipped_image.jpg', language)
    
    elif "Orientation in degrees: 90" in osd:
        im = Image.open('/home/pi/deskewed_image.jpg')
        angle = 90
        out = im.rotate(angle)
        out.save("/home/pi/flipped_image.jpg")
        text = text_extraction('/home/pi/flipped_image.jpg', language)

    elif "Orientation in degrees: 270" in osd:
        im = Image.open('/home/pi/deskewed_image.jpg')
        angle = 90
        out = im.rotate(angle)
        out.save("/home/pi/flipped_image.jpg")
        text = text_extraction('/home/pi/flipped_image.jpg', language)
        
    else:
        text = text_extraction('/home/pi/deskewed_image.jpg', language)
    
    text = mistake_removal(text)
    
    if 'bul' in language:
        language = 'bg'
    elif 'eng' in language:
        language = 'en'
        
    gtts_speak(str(text), language)
    

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