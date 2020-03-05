


import speech_recognition as sr
from PIL import Image,ImageTk



import os



import threading
import time
import  tkinter as tk

SIZE = (300,300)
PADDING_IMAGE_X = 5
PADDING_IMAGE_Y = 5
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))
image_list=[]

class ImageTestDyslexia(tk.Frame):
 
    def __init__(self,master):
      
        tk.Frame.__init__(self,master)
        self.Question = tk.Label(self,font=('Helvetica', '14'),text="Hello, \nSelect the picture that represents a car ?")
        self.createWindow()

    # processing function 
    def initRecognition(self,word,*args,**kwargs):
        r=sr.Recognizer()
        mic= sr.Microphone()
        print("speak")
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                tk.messagebox.showinfo('Message',"You didnt speak anything please speak again")
        
                
        try:
            recognisedPhrase= r.recognize_google(audio)
            if recognisedPhrase == word:
                print(True)
            else:
                print(False)
        except sr.UnknownValueError:
            tk.messagebox.showinfo('Message',"What you spoke didnt make any sense try one more time ")
 
        
    # Interface creation function
    def createWindow(self):
        im_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\boat.png")
        im_1 = im_1.resize(SIZE,Image.ANTIALIAS)
        photo_1 = ImageTk.PhotoImage(im_1) 
        image_list.append(photo_1)
        im_2 = Image.open(BASE_DIR+"\\tinkerpro\\img\\car.png")
        im_2 = im_2.resize(SIZE,Image.ANTIALIAS)
        photo_2 = ImageTk.PhotoImage(im_2) 
        image_list.append(photo_2)
        im_3 = Image.open(BASE_DIR+"\\tinkerpro\\img\\computer.png")
        im_3 = im_3.resize(SIZE,Image.ANTIALIAS)
        photo_3 = ImageTk.PhotoImage(im_3) 
        image_list.append(photo_3)

        im_4 = Image.open(BASE_DIR+"\\tinkerpro\\img\\windmill.png")
        im_4 = im_4.resize(SIZE,Image.ANTIALIAS)
        photo_4 = ImageTk.PhotoImage(im_4)
        image_list.append(photo_4) 
        # here, image option is used to 
        # set image on button 
        button_1 = tk.Button(self, image = photo_1,command=lambda:threading.Thread(target=self.initRecognition,args=("boat"),daemon=True).start() )
        button_1.grid(row=3,column=5,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y)
        button_2 = tk.Button(self, image = photo_2,command=lambda: threading.Thread(target=self.initRecognition,args=("car"), daemon=True).start())
        button_2.grid(row=3,column=6,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 
        button_3 = tk.Button(self, image = photo_3,command=lambda: threading.Thread(target=self.initRecognition,args=("computer"),daemon=True).start())
        button_3.grid(row=4,column=5,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 
        button_4 = tk.Button(self, image = photo_4,command=lambda: threading.Thread(target=self.initRecognition,args=("windmill"),daemon = True).start())
        button_4.grid(row=4,column=6,ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y) 
        tk.Button(self,text="i am gud man",command = lambda : threading.Thread(target= self.change,daemon=True).start() ).grid(row=5,column=6)

        
        self.Question.grid(row=2,column = 0,sticky=tk.W,padx = 20,pady=20)

    def change(self):
        count =0;
        for i in range(0,10):
            time.sleep(2)
            count +=1
            self.Question['text'] = count
        
        

    

  
        