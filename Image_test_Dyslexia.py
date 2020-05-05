import speech_recognition as sr
from PIL import Image, ImageTk
import os
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import random
import startingPage
import learningtest
from gtts import gTTS 
from playsound import playsound
import evaluation
language = 'en'


TEST_DURATION = 180  #seconds genarally 3 minutes 
SIZE = (250, 250)
PADDING_IMAGE_X = 10
PADDING_IMAGE_Y = 10
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))
image_list = []
image_list_other= []
image_list_second=[]
imageCorrectAnswers = 0
totalImageAnswers = 0

class ImageTestDyslexia(tk.Frame):
    def __init__(self, master,*awrgs,**kwargs):
        tk.Frame.__init__(self, master,bg = '#5CC7B2')
   
        self.Question = tk.Label(self, font=('Times', '20', 'normal'), text="",bg = '#5CC7B2')
        tk.Label(self, font=('Times',24,'normal'), text="Initial Sound Fluency Test",bg = '#5CC7B2').grid(
            row=0, column=1)
        self.RECORDINGCOUNT = 0
        self.app = list(awrgs)
        print(self.app)
        self.instruction_label_counter=1
        self.init_result = False
        self.nextFlag = True
        self.images_dic = ['boat', 'car', 'computer', 'dog',
                            'home', 'cycle', 'tree', 'windmill','cat','fan','apple']
        self.done_Timer_Flag=False
        self.image_sounds_dict ={}
        self.lock = threading.Lock()
        self.answered_flag = True
        self.crct_answered = 0
        self.total_questions = 0
        self.button_list=[]
        self.button_list_second=[]
        self.image_string=[]
        self.quick_instruction_label = tk.Label(self,font=('Times','18','normal'),text="",bg='#61F8D4')
        self.selected_word =  None
        self.speaker_label = None
        self.createWindow()

    # processing function
    def initRecognition(self, word,toggle, *args, **kwargs):
        
        audio_flag=True
        r = sr.Recognizer()
        mic = sr.Microphone()
        print("speak")
        self.quick_instruction_label['text'] = "Say it loud I am listening"
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
                
            except sr.WaitTimeoutError:
                audio_flag=False
                if toggle:
                    threading.Thread(target=self.initRecognition,args=(word,False),daemon=True).start()
                    exit()
                tk.messagebox.showinfo(
                    'Message', "You didnt speak anything please speak again")

        if audio_flag:
            try:
                self.quick_instruction_label['text'] = "Processing....."
                recognisedPhrase = r.recognize_google(audio)
                print(recognisedPhrase)
                if recognisedPhrase.lower() == word.lower():
                    self.init_result = True
                    if(self.selected_word==word):
                        self.crct_answered+=1
                    else:
                        self.crct_answered+=0.5

                    print('true')
                else:
                    self.init_result = False
                    print('False')
            except sr.UnknownValueError:
                tk.messagebox.showinfo(
                    'Message', "What you spoke didnt make any sense try one more time ")
            finally:
                self.quick_instruction_label['text'] = "Almost done!!!"
                print(self.button_list)
                for temp_btn in self.button_list:
                    temp_btn.grid_forget()
                self.answered_flag=True
                self.button_list.clear()
                self.image_string.clear()




                
        


    # Interface creation function

    def createWindow(self):
        self.Question.grid(row=1, column=1, sticky=tk.W, padx=15, pady=20)
        self.Question['text'] = "Hey welcome to the test if you are ready then lets start the test....."

        threading.Thread(target=self.instructionThread,args=(),daemon=True).start()
        # im_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\speaker.png")
        # im_1 = im_1.resize(SIZE,Image.ANTIALIAS)
        # photo_speaker = ImageTk.PhotoImage(im_1)
        # self.speaker_label = tk.Label(self,image= photo_speaker,)
        # self.speaker_label.grid(row=1,column=2,sticky=tk.W)         
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
        print("Next button flag invoker is called")
        self.nextFlag = True
    def repeatBtn(self,btn,nextbtn,instruction_label_dic_copy):

        btn.grid_forget()
        nextbtn['text'] = "Next"
        nextbtn.grid(
            row=3,
            column=1
        )
        self.instruction_label_counter = 2
        self.Question['text'] = instruction_label_dic_copy[self.instruction_label_counter]        
 

    def timerThread(self,*awrgs,**kwargs):
      tag="TimerThread"
      print(tag+ " I am called")
      time_interval = TEST_DURATION
      self.lock.acquire()
      self.done_Timer_Flag = False
      self.lock.release()
      time.sleep(time_interval)
      self.lock.acquire()
      self.done_Timer_Flag = True
      self.lock.release()
      print(tag+"I am ending master test should also end ......")


    def instructionThread(self, *args, **kwargs):
        
        tag="Instruction Thread" #it is an variable fot debugging
        #image_list global variable to hold images reference
        instruction_label_dic = {
            1:"Hello welcome to the test Initial Fluency Test",
            2:"This test will go on for three minutes",
            3:"We will be presenting you 4 pictures, we will name each picture",
            4:"Then we will ask for the name of the picture that starts with the sound ",
            5:"Then you should point to the picture or say it  orally",
            6:"If you want to repeat the instruction then we will if not lets start the test!",
            

        }
        im_1_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\flame-page-under-construction.png")
        im_1_1 = im_1_1.resize((350,350),Image.ANTIALIAS)
        image_list_other.append(ImageTk.PhotoImage(im_1_1))
        image_label = tk.Label(self,
            image = image_list_other[0],
            background="#5CC7B2",
        )
        image_label.grid(
            row=2,
            column=1
        )
 
        button = tk.Button(self, font=('Times', 15), text="Next", relief='ridge', command=self.nextBtn)
        button_repeat = tk.Button(self, font=('Times', 15), text="Repeat", relief='ridge', command=lambda: self.repeatBtn(button_repeat,button,instruction_label_dic))
        button.grid(row=3, column=1)
        path=BASE_DIR+"\\tinkerpro\\recording"
        self.instruction_label_counter=1
        while True:
            if self.nextFlag and self.instruction_label_counter<7:
                print("I am inside the main bosidike")
                
                  
                   
 
                self.Question['text'] = instruction_label_dic[self.instruction_label_counter]
                button['state'] = tk.DISABLED
                myobj = gTTS(text=instruction_label_dic[self.instruction_label_counter], lang=language, slow=False,) 
                myobj.save("recording"+str(self.RECORDINGCOUNT)+".mp3")
                playsound("recording"+str(self.RECORDINGCOUNT)+".mp3")
                os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                self.RECORDINGCOUNT+=1
                button['state'] = tk.NORMAL
                
                print(path)
                
                if self.instruction_label_counter==6:
                    button['text']="Lets Start!"
                    button.grid(row=3,column=0)
                    button_repeat.grid(row=3,column=2)
                if self.instruction_label_counter==3:
                    image_label.grid_forget()
                    button.grid(row=4,column=1)
                    temp_int_row = 3
                    temp_int_column=-2
                    for i in range(0, 4):
                        temp = random.choice(self.images_dic)
                        while temp in  self.image_string:
                            temp  = random.choice(self.images_dic)
                        self.image_string.append(temp) #randomly selected images basically a string 
                        im = Image.open(BASE_DIR+"\\tinkerpro\\img\\"+self.image_string[i]+".png").resize(SIZE,Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(im) 
                        image_list_second.append(photo)
                        btn_temp_second  = tk.Button(self, image = photo,borderwidth=10,command = lambda: threading.Thread(target=self.initRecognition,args=(self.image_string[i],True),daemon=True).start())
                        if temp_int_column==2:
                            temp_int_row=4
                            temp_int_column = 0
                        else:
                            temp_int_column+=2
                        btn_temp_second.grid(row = temp_int_row,column = temp_int_column,padx=PADDING_IMAGE_X,pady=PADDING_IMAGE_Y)
                        self.button_list_second.append(btn_temp_second)
                    
                    self.nextFlag = False
                    count=0
                    
                    while True:
                        if count!=4 and not self.nextFlag:
                            self.button_list_second[count].configure(background='red')
                            myobj = gTTS(text=self.image_string[count], lang=language, slow=False,) 
                            myobj.save("recording"+str(self.RECORDINGCOUNT)+".mp3")
                            playsound("recording"+str(self.RECORDINGCOUNT)+".mp3")
                            os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                            self.RECORDINGCOUNT+=1
                            
                            self.button_list_second[count].configure(background='white')
                            count+=1
                        else:
                            for item in self.button_list_second:
                                item.grid_forget()
                            image_list_second.clear()
                            self.button_list_second.clear()
                            button.grid(row=3,column=1)
                            image_label.grid(row=2,column=1)
                            break
                    
                        
                      

                self.instruction_label_counter+=1 
                
                
                self.nextFlag=False
            elif self.nextFlag and self.instruction_label_counter>6:
                break
        image_label.grid_forget()
        button.grid_forget()
        self.Question['text'] = "Select the picture that resembles a "
        threading.Thread(target=self.timerThread,args=(),daemon=True).start()
        temp_variable_timer = False
        self.quick_instruction_label.grid(row=2,column=1)
        while not temp_variable_timer:

            if self.answered_flag:
                print(tag+"I am called")
                temp_int_row = 3
                temp_int_column=-2
                self.quick_instruction_label['text']="Listen Carefully .."
                self.button_list.clear()
                self.image_string.clear()
                for i in range(0, 4):
                    
                    temp = random.choice(self.images_dic)
                    while temp in  self.image_string:
                        temp  = random.choice(self.images_dic)
                    self.image_string.append(temp) #randomly selected images basically a string 
                    im = Image.open(BASE_DIR+"\\tinkerpro\\img\\"+self.image_string[i]+".png").resize(SIZE,Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(im) 
                    image_list.append(photo)
                    if temp_int_column==2:
                        temp_int_row=4
                        temp_int_column = 0
                    else:
                        temp_int_column+=2
                    btn_temp  = tk.Button(self, image = photo,borderwidth=20,command = lambda: threading.Thread(target=self.initRecognition,args=(self.image_string[i],True),daemon=True).start())
                    btn_temp.grid(row = temp_int_row,column = temp_int_column,padx=PADDING_IMAGE_X,pady=PADDING_IMAGE_Y)
                    self.button_list.append(btn_temp)
                    self.answered_flag  = False
                    print(btn_temp)
                rand_temp = random.randint(0,3)
                for count in range(0,4):
                    self.button_list[count].configure(background='red')
                    myobj = gTTS(text=self.image_string[count], lang=language, slow=False,) 
                    myobj.save("recording"+str(self.RECORDINGCOUNT)+".mp3")
                    playsound("recording"+str(self.RECORDINGCOUNT)+".mp3")
                    os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                    self.RECORDINGCOUNT+=1
                            
                    self.button_list[count].configure(background='white')
                

                
                self.selected_word = self.image_string[rand_temp]
                self.Question['text'] = "Select the image which starts with the sound ...." + "//"+self.selected_word[:2]+"//"
                self.quick_instruction_label['text'] = "Select the image and say it loud that starts with "+"//"+self.selected_word[:2]+"//" + " sound"
               
               
                

            
            self.lock.acquire()
            self.total_questions +=1
            temp_variable_timer = self.done_Timer_Flag
            self.lock.release()
        print(self.image_string)   
        print(self.crct_answered)
        imageCorrectAnswers = self.crct_answered
        totalImageAnswers = self.total_questions
        

        self.app[0].switchFrame(learningtest.LearningTest,self)###########################################
