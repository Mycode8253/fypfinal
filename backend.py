import speech_recognition as sr
from tkinter import messagebox

def initRecognition(word):
    r=sr.Recognizer()
    mic= sr.Microphone()
    print("speak")
    with mic as source:
        try:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            messagebox.showinfo('Message',"You didnt speak anything please speak again")
       
            
    try:
        recognisedPhrase= r.recognize_google(audio)
        if recognisedPhrase == word:
            print(True)
        else:
            print(False)
    except sr.UnknownValueError:
        messagebox.showinfo('Message',"What you spoke didnt make any sense try one more time ")
    

def printVersion():
    print(sr.__version__)



        




