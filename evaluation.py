
import tkinter as tk
import tkinter.ttk as ttk
import Image_test_Dyslexia
import learningtest
from PIL import Image, ImageTk
import os
from gtts import gTTS
from playsound import playsound
import threading


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))

image_list_other=[]
language="en"
path=BASE_DIR+"\\tinkerpro\\recordevaluation"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))


class Evaluation(tk.Frame):
    def __init__(self, master,*awrgs,**kwargs):
        tk.Frame.__init__(self, master,bg = '#EA696B')
       
        self.Main_Heading = tk.Label(self, font=('Times', '24', 'bold'), text="",bg = '#EA696B',fg='#FCF7D9')
        self.Label1 = tk.Label(self, font=('Times',24,'normal'), text="Evaluation",bg = '#EA696B',fg='#FCF7D9')
        self.Label1.grid(
            row=2, column=1,pady=2)
        self.app = awrgs[0]
        self.app.configure(background="#EA696B")
        self.Main_Heading.grid(row=0,column=1,pady=2)
        self.Main_Heading["text"] = "Evaluation"
        self.RECORDINGCOUNT = 0
        
        im_1_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\mirage-success.png")
        im_1_1 = im_1_1.resize((80,150),Image.ANTIALIAS)
        image_list_other.append(ImageTk.PhotoImage(im_1_1))
        self.image_label = tk.Label(self,
            image = image_list_other[0],
            bg="#EA696B",)
        global path
        self.image_label.grid(row=1,column=1,pady=2)
        self.Label1['text'] = "Hey you have done really good so far"
        threading.Thread(target=self.processThread,args=(),daemon=True).start()
      


    def processThread(self,*args,**kwargs):
        
        myobj = gTTS(text=self.Label1['text'], lang=language, slow=False,) 
        myobj.save("recordevaluation"+str(self.RECORDINGCOUNT)+".mp3")
        playsound("recordevaluation"+str(self.RECORDINGCOUNT)+".mp3")
        os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
        self.RECORDINGCOUNT+=1
        Label2 = tk.Label(self, font=('Times',24,'normal'), text="Game",bg = '#EA696B',fg='#FCF7D9')
        Label2.grid(
            row=3, column=1,pady=2)
        Label2['text'] = " Here are the following results "
        Label3 = tk.Label(self, font=('Times',24,'normal'), text="Game",bg = '#EA696B',fg='#FCF7D9')
        Label3.grid(
            row=4, column=1,pady=2)
        Label3['text'] = " Here are the following results "
        Label4 = tk.Label(self, font=('Times',24,'normal'), text="Game",bg = '#EA696B',fg='#FCF7D9')
        Label4.grid(row=5, column=1,pady=2)
        Label4['text'] = " Here are the following results "
        print("I am ending people")




        

    





        print(Image_test_Dyslexia.imageCorrectAnswers)
