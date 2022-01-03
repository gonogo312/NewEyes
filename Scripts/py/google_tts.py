from textblob import TextBlob
from langdetect import detect
from gtts import gTTS
import os


def gtts_speak(text):
    
    #var = detect(text)
    #print(var)
    text = text.replace("- ", "")
    text = text.replace("-  ", "")
    blob = TextBlob(text)
    print(blob)
    
    #translator= Translator(to_lang="Bulgarian")
    #translation = translator.translate(text)
    #print(translation)
    
    if text != "":
        #tts = gTTS(text, lang=var)
        #print(detect(text))
        language = detect(text)
        tts = gTTS(text, lang=language)
        tts.save('page.mp3')
        os.system('mpg321 page.mp3 &')

    else:
        errorMessages = ["няма нищо пред вас!",
                         "съжалявам, но няма нищо за четене!",
                         "няма нищо за четене, пробвайте да направите нова снимка!"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        tts = gTTS(chosen_message, lang = 'bg')
        tts.save('error.mp3')
        os.system('mpg321 error.mp3 &')