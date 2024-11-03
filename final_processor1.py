from email import message
from re import T
from gtts import gTTS
import speech_recognition as sr
import os
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import wolframalpha 
import wikipedia
import datetime
import warnings
import tkinter as tk
from tkinter import ttk
from tkinter import END
from tkinter import INSERT
import smtplib
#import face_recognition
import cv2
import csv
import time
from time import sleep
from csv import writer
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import frame_viewer as frview
# from pydub import AudioSegment
# from pydub.playback import play
# import simpleaudio as sa
import vlc
#import RPi.GPIO as GPIO

 


from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('job_intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.8
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
    
def speak(text):
    tts = gTTS(text=text, lang="en")
    file = "sound.mp3"
    tts.save(file)
    
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new_path(file)
    player.set_media(media)
    player.play()
    while player.get_state() != vlc.State.Ended:
        time.sleep(1)
    player.stop()
    vlc_instance.release()
    os.remove(file)
    
def internet_audio():
    app_id = "44YXHU-TV6AJRQ6HT" 
    text=Message_audio
    try:
        client = wolframalpha.Client(app_id) 

        res = client.query(text) 

        answer = next(res.results).text 
        speak(answer)
    except:
        try:
           result = wikipedia.summary(text, sentences = 1) 
           speak(result)  
        except wikipedia.exceptions.PageError:
            speak('Sorry cannot understand')  
            reply()
        except wikipedia.exceptions.DisambiguationError:
            speak('Sorry cannot understand. Can you be more specific')  
            reply()
              
def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        # r.energy_threshold()
        print("say anything : ")
        audio= r.listen(source)
        try:
            global text
            text = r.recognize_google(audio)
            print(text)
        except:
            print("sorry could not recognize ")
            speak("Could not understand ,please come again")
            get_audio()
    return text
        
def timeaudio():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(current_time)    
        
def date_today():
    today = datetime.date.today()
    d1 = today.strftime("%d/%m/%Y")
    speak(d1)
   
def getResponse_audio(ints, intents_json):
    global tag
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    global result
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            speak(result)
            break    
    if(tag=='goodbye'):
        process()
    elif(tag=='internet_audio'):
        internet_audio()
    return result

# def recognise():
#     print("[INFO] loading encodings + face detector...")
#     data = pickle.loads(open("encodings.pickle", "rb").read())
#     detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#         # initialize the video stream and allow the camera sensor to warm up
#     print("[INFO] starting video stream...")
#     vs = VideoStream(src=0).start()
#     # vs = VideoStream(usePiCamera=True).start()
#     now=datetime.datetime.now() 
#     current_data=now.strftime("%Y-%m-%d")
#         # start the FPS counter
#     fps = FPS().start()
#     t0 = time.time()
#         # loop over frames from the video file stream
#     while True:
#             # grab the frame from the threaded video stream and resize it
#             # to 500px (to speedup processing)
#             frame = vs.read()
#             frame = imutils.resize(frame, width=500)
#             # convert the input frame from (1) BGR to grayscale (for face
#             # detection) and (2) from BGR to RGB (for face recognition)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             # detect faces in the grayscale frame
#             rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
#                 minNeighbors=5, minSize=(30, 30),
#                 flags=cv2.CASCADE_SCALE_IMAGE)
#             # OpenCV returns bounding box coordinates in (x, y, w, h) order
#             # but we need them in (top, right, bottom, left) order, so we
#             # need to do a bit of reordering
#             boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#             # compute the facial embeddings for each face bounding box
#             encodings = face_recognition.face_encodings(rgb, boxes)
#             names = []
#             # loop over the facial embeddings
#             for encoding in encodings:
#                 # attempt to match each face in the input image to our known
#                 # encodings
#                 matches = face_recognition.compare_faces(data["encodings"],
#                     encoding)
#                 name = "Unknown"
#                 # check to see if we have found a match
#                 if True in matches:
#                     # find the indexes of all matched faces then initialize a
#                     # dictionary to count the total number of times each face
#                     # was matched
#                     matchedIdxs = [i for (i, b) in enumerate(matches) if b]
#                     counts = {}
#                     # loop over the matched indexes and maintain a count for
#                     # each recognized face face
#                     for i in matchedIdxs:
#                         name = data["names"][i]
#                         counts[name] = counts.get(name, 0) + 1
#                     # determine the recognized face with the largest number
#                     # of votes (note: in the event of an unlikely tie Python
#                     # will select first entry in the dictionary)
#                     name = max(counts, key=counts.get)
#                 # update the list of names
#                 names.append(name)
#                 if name =="Unknown":
#                    print('Unknown Detected')
#                    speak('Sorry You are not in my database')
#                 else:
#                    print("Hello "+name)
#                    speak("Hello "+name)
      
#             # loop over the recognized faces
#             for ((top, right, bottom, left), name) in zip(boxes, names):
#                 # draw the predicted face name on the image
#                 cv2.rectangle(frame, (left, top), (right, bottom),
#                     (0, 255, 0), 2)
#                 y = top - 15 if top - 15 > 15 else top + 15
#                 cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
#                     0.75, (0, 255, 0), 2)
                
            
#             t1 = time.time() # current time

#             num_seconds = t1 - t0 # diff

#             if num_seconds > 3:  # e.g. break after 5 seconds
#                  break
   
#             # update the FPS counter
#             fps.update()

#         # stop the timer and display FPS information
  
#     fps.stop()
#     print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#     print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

#         # do a bit of cleanup
#     cv2.destroyAllWindows()
#     vs.stop()
      

def reply():
       global Message_audio
       Message_audio = get_audio()
       Message_audio=Message_audio.lower()
       ints=predict_class(Message_audio, model)
       if ints==[]:
           ints=[{'intent': 'internet_audio', 'probability': '0.9999997615814209'}]             
       getResponse_audio(ints, intents) 
       if 'bye charm' in Message_audio:
         process()
       if 'time' in Message_audio:
         timeaudio()
       elif 'date' in Message_audio:
         date_today()
       elif 'suggestion' in Message_audio:
            speak('What suggestion would you like to give ?')
            suggestion_audio=get_audio()
            smtplibObj=smtplib.SMTP('smtp.gmail.com', 587)
            smtplibObj.ehlo()
            smtplibObj.starttls()
            smtplibObj.login("pavitnarang14@gmail.com" ,"glzininpfrxdjdao")
            smtplibObj.sendmail("pavitnarang14@gmail.com","pavitnarang0512@gmail.com",suggestion_audio)
            smtplibObj.quit()
            speak('Your suggestion has been sent')
            
print("CHARM is running")



def person():
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()  # Assuming camera source is 2, adjust as needed
    time.sleep(2.0)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    person_detected = False

    try:
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)  # Resize frame for faster processing (optional)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                center = x + w // 2, y + h // 2
                radius = w // 2
                frame = cv2.circle(frame, center, radius, (0, 255, 0), 3)

            
            if len(faces) > 0:
                print("Person Detected")
                person_detected = True
                break
            else:
                print("Person Detected")
                person_detected = False
                break

    except Exception as e:
        print(f"Exception in person(): {e}")
        # Optionally handle or log the exception here

    finally:
        
        vs.stop()

    return person_detected

def process():
    if person()==True:
        reply()
    elif person()==False:
        process()

process()




