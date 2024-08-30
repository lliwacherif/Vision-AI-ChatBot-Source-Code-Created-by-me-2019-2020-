from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
now = datetime.now()
currentYear = now.year
currentMonth = now.month
currentDay = now.day
currentHour = now.hour
currentMin = now.minute
import webbrowser
import speech_recognition as sr
import time
import pyttsx3
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
from twilio.rest import Client

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def speak(text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 175)                          
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
speak("stand by for Facial and iris scan.")

#face scan for unloking
import cv2
camera_port = 0
ramp_frames = 30

camera = cv2.VideoCapture(camera_port)

def get_image():
    retval, im = camera.read()
    return im


for i in range(ramp_frames):
    temp = get_image()

print("_scanning...")

camera_capture = get_image()
file = "test.jpg"
cv2.imwrite(file, camera_capture)

del camera
print("_Scan completed")

def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded
def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding
def classify_face(im):
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    # Display the resulting image
    i = 0
    while i < 100 :
        return face_names
        i =i+1

print(classify_face("test.jpg"))
def speak(text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 190)                          
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

if "liwa cherif" in classify_face("test.jpg") :
    speak("facial and iris scan accepted.")
    if currentHour<= 12:
        speak("good morning boss.")
    else :
        speak("good evening boss.")

    def authenticate_google():
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        return service

    def get_events(n, service):
        now = datetime.utcnow().isoformat() + 'Z' 
        speak("here it is  the upcoming events sir.")
        print(f'Getting the upcoming {n} events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=n, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print("_No upcoming events found.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


    service = authenticate_google()
    get_events(2, service)        
    wake = ("vision")
    while True :
        def speak(text):
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate', 190)                          
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()
        def get_audio():
	        r = sr.Recognizer()
	        with sr.Microphone() as source:
		        audio = r.listen(source)
		        said = ""

		        try:
		            said = r.recognize_google(audio)
		            print(said)
		        except Exception as e:
		            print("Exception: " + str(e))

	        return said

        print("listening")	
        text = get_audio()
        if text.count(wake) > 0:
            speak("yes sir.")
            text = get_audio()
        
            if ( "what" in text ) and ("your" in text ) and ("name" in text) :
                speak("my name is vision .")
                   
            #search protocol    
            elif ("search" in text ) or ("open google" in text ) :

                new=2

                tabUrl="http://google.com/?#q=";
                speak("what is the search query?")
                text = get_audio()
                term= text

                webbrowser.open(tabUrl+term,new=new);
                speak("i found these results on the web , boss.")

            elif ("present your self" in text ) or ("what are you" in text ) or ("who are you" in text ) :
                speak("I'm vision . an artificial intelligence security and defence system made by Mr cherif.")

            #send emails protocol    
            elif ("send" in text ) and ("email" in text) :
                speak("Activating postman protocol.")
                speak("ok , who is the receiver?") 
                print("_ok , who is the receiver?")
                R=input('')
                speak("give me his email please")
                print("_give me his email please :")
                E=input('')
                speak("and the subject is...")
                print("_and the subject is :")
                S=input('')
                speak("now you can write the messege sir")
                print("_now write the messege :")
                M=input('')
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                email = 'liwacherif200@gmail.com'
                speak("please enter the Password sir")
                password = input()
                send_to_email = E
                subject = S 
                message = M

                msg = MIMEMultipart()
                msg['From'] = 'Cherif Liwa'
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string() 
                server.sendmail(email, send_to_email, text)
                server.quit()
                speak("ok boss , i'm sending it ... It should have been sent now.")
                speak("check the 'sent' box in your email please") 

            #open apps in browser
            elif  ("open" in text ) and ("Google Docs" in text ) :
                new=2

                tabUrl="http://docs.google.com/document/u/0/";
                webbrowser.open(tabUrl,new=new);
                speak("here it is the google docs.")
            elif  ("open" in text ) and ("Google Drive" in text ) :
                new=2

                tabUrl="http://drive.google.com/drive/my-drive";
                webbrowser.open(tabUrl,new=new);
                speak("here it is the google drive.")
            elif  ("open"in text ) and ("YouTube Studio"in text) :
                new=2

                tabUrl="http://studio.youtube.com/channel/UCS_Na7aiBhR6CgRlV3l6VeQ";
                webbrowser.open(tabUrl,new=new);
                speak("here it is the youtube studio sir.")
            elif (("events" in text ) or ("event" in text )) and (("what's" in text ) or ("do i have" in text ) or ("show me" in text )) :
                def get_events(n, service):
                    now = datetime.utcnow().isoformat() + 'Z' 
                    speak("Getting the upcoming events sir.")
                    print(f'Getting the upcoming {n} events')
                    events_result = service.events().list(calendarId='primary', timeMin=now,
                                                        maxResults=n, singleEvents=True,
                                                        orderBy='startTime').execute()
                    events = events_result.get('items', [])

                    if not events:
                        speak('No upcoming events found sir!')
                        print("_No upcoming events found sir")
                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        print(start, event['summary'])
                        speak("here's what i found sir")


                service = authenticate_google()
                get_events(2, service)
            #make new project
            elif (("open" in text ) or ("make" in text )) and (("new folder" in text) or ("new project" in text )) :   
                speak ("do like me to save it in my main directory sir?") 
                text = get_audio()
                if ("yes" in text) :
                    os.mkdir("new project")
                    speak("the new project has been created successfully sir.")
                else :
                    os.chdir("Bureau")
                    os.mkdir("new project")
                    speak("the new project has been created successfully sir.")
            else :
                speak("i dont get that , sir")  
else :
    speak("facial and iris scan non accepted.")
    speak("please back away ...")
    speak("i'm contacting Mr cherif now.")
    print("VISION<-------------->Mr cherif")
    R="Mr cherif"
    E="liwacherif200@gmail.com"
    S="A possible system hack attempt" 
    M="Someone tried to log in to the system. facial data non accepted"
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    email = 'liwacherif200@gmail.com'
    password = "12300liwa"
    send_to_email = E
    subject = S 
    message = M

    msg = MIMEMultipart()
    msg['From'] = 'VISION'
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() 
    server.sendmail(email, send_to_email, text)
    server.quit()
         
account_sid = '#########'
auth_token = '##########'
client = Client(account_sid, auth_token)


from_whatsapp_number='whatsapp:+1415528886'
to_whatsapp_number='whatsapp:+21694192570'

message = client.messages.create(body="A possible system hack attempt , Someone tried to log in to the system" ,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
print(message.sid)
