import speech_recognition as sr
from PIL import Image, ImageTk
import os
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import random

SIZE = (300, 300)
PADDING_IMAGE_X = 5
PADDING_IMAGE_Y = 5
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))
image_list = []


class ImageTestDyslexia(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master,)
        self.Question = tk.Label(self, font=('Times', '14', 'bold'), text="")
        tk.Label(self, font=('system'), text="Initial Sound Fluency Test").grid(
            row=0, column=1)
        
        self.init_result = False
        self.nextFlag = True
        self.images_dic = ['boat', 'car', 'computer', 'dog',
                            'home', 'ramen', 'tree', 'windmill',
                            'workspace']
        self.done_Timer_Flag=False
        self.image_sounds_dict ={}
        self.lock = threading.Lock()
        self.answered_flag = True
        self.crct_answered = False
        self.total_questions = False
        self.button_list=[]
        
        self.createWindow()

    # processing function
    def initRecognition(self, word, *args, **kwargs):
        audio_flag=True
        r = sr.Recognizer()
        mic = sr.Microphone()
        print("speak")
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
                
            except sr.WaitTimeoutError:
                audio_flag=False
                tk.messagebox.showinfo(
                    'Message', "You didnt speak anything please speak again")
                
                
        if audio_flag:
            try:
                recognisedPhrase = r.recognize_google(audio)
                if recognisedPhrase == word:
                    self.init_result = True
                    print('true')
                else:
                    self.init_result = False
                    print('False')
            except sr.UnknownValueError:
                tk.messagebox.showinfo(
                    'Message', "What you spoke didnt make any sense try one more time ")
            finally:
                print(self.button_list)
                for temp_btn in self.button_list:
                    temp_btn.grid_forget()
                    self.answered_flag=True


                
        


    # Interface creation function

    def createWindow(self):
        self.Question.grid(row=1, column=1, sticky=tk.W, padx=15, pady=20)
        self.Question['text'] = "Hey welcome to the test if you are ready then lets start the test....."
        threading.Thread(target=self.instructionThread,args=(),daemon=True).start()
        
        # GUI decoration code will come here just to make the whole thing to look pretty  
        '''
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
        '''
    

    def nextBtn(self):
        self.nextFlag = True

    def timerThread(self,*awrgs,**kwargs):
      tag="TimerThread"
      print(tag+ " I am called")
      time_interval = 180
      self.lock.acquire()
      self.done_Timer_Flag = False
      self.lock.release()
      time.sleep(time_interval)
      self.lock.acquire()
      self.done_Timer_Flag = True
      self.lock.release()
      print(tag+"I am ending master test should also end ......")
    

    def instructionThread(self, *args, **kwargs):
        #image_list global variable to hold images reference
        instruction_label_dic = {
            1:"Hello welcome to the test Initial Fluency Test",
            2:"This test will go on for three minutes",
            3:"We will be presenting you 4 pictures, we will names each picture",
            4:"Then we will ask for the name of the picture that starts with the sound ###",
            5:"Then you should point to the picture or say it  orally",
            6:"If you want to repeat the instruction then we will if not lets start the test!",

        }
        button = tk.Button(self, font=('Calibre', 10), text="Next", relief='ridge', command=self.nextBtn)
        button.grid(row=2, column=1)
        instruction_label_counter = 1
        while True:
            if self.nextFlag and instruction_label_counter<7:
                self.Question['text'] = instruction_label_dic[instruction_label_counter]
                if instruction_label_counter==6:
                    button['text']="Lets Start!"
                instruction_label_counter+=1
                
                self.nextFlag=False
            elif self.nextFlag and instruction_label_counter>6:
                break

        button.grid_forget()
        image_string=[]
        threading.Thread(target=self.timerThread,args=(),daemon=True).start()
        temp_variable_timer = False
        while not temp_variable_timer:
            self.lock.acquire()
            temp_variable_timer = self.done_Timer_Flag
            
            self.lock.release()
            if self.answered_flag:
                print("Instructio thread"+"I am called")
                for i in range(0, 4):
                    temp = random.choice(self.images_dic)
                    while temp in image_string:
                        temp  = random.choice(self.images_dic)
                    image_string.append(temp) #randomly selected images basically a string 
                    im = Image.open(BASE_DIR+"\\tinkerpro\\img\\"+image_string[i]+".png").resize(SIZE,Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(im) 
                    image_list.append(photo)
                    btn_temp  = tk.Button(self, image = photo,command = lambda: threading.Thread(target=self.initRecognition,args=(image_string[i]),daemon=True).start(),background='red')
                    btn_temp.grid(row = 3 if(i>=2) else 4,column = (0 if((i%2)==0) else 1) +(i%2),ipadx=PADDING_IMAGE_X,ipady=PADDING_IMAGE_Y)
                    self.button_list.append(btn_temp)
                    self.answered_flag  = False
                    print(btn_temp)
        print(image_string)
        self.Question['text'] = "Select the image which starts with the sound ...." 
