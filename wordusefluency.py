import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
import speech_recognition as sr
import time
import evaluation
from PIL import Image, ImageTk
import os
from gtts import gTTS
from playsound import playsound
language='en'

TEST_DURATION=60


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('img')))
image_list_other=[]

totalquestions=0
crctquestions=0


class WordUseFluency(tk.Frame):

    def __init__(self,master,*args,**kawrgs):
        
        tk.Frame.__init__(self,master,bg="#3E8188")

        tk.Label(self, font=('Times',24,'normal'), text="Word Use Fluency Test",bg="#3E8188",fg="white").grid(row=0, column=1)
        self.instruction_label = tk.Label(self, font=('Times', '20', 'normal'),bg="#3E8188",fg="white", text="Hey Hello! you came so far...",)
        self.instruction_label.grid(row=1,column=1,pady=5)
        self.helper_label = None
        self.app=list(args)
        print(args)
        self.app[0].configure(bg="#3E8188")
        #Helpfull variables
        self.instruction_dict = {
            1:"Hey welcome to  Word Use Fluency Test",
            2:"Listen to me carefully, How I use this word 'Green' in a sentense, \n The grass is green ",
            3:"Here is another word ' jump ' \n  I would like to jump ",
            4:"Now your turn use the word 'rabbit' ",
            5:"Good! You have done it so lets start the test...", 
        }
        self.word_dict={
            1:"rabbit",
            2:"brush",
            3:"banana",
            4:"nose",
            5:"hen",
            6:"eggs",
            7:"bath",
            8:"home",
            9:"chair",
            10:"shout",
            11:"apple",
        }
        self.RECORDINGCOUNT = 0
        self.nextButtonFlag=False
        self.nextButton = None
        self.instruction_counter = 0
        self.change_label = True
        self.countNextButton = 0
        self.tutorialFlag = True
        self.completed_listening_flag = False
        self.threadLock = threading.Lock()
        self.failed_flag = False
        self.letter_label= None
        self.repeatFlag = False
        self.time_complete_flag=False
        self.image_label=None
        self.total_questions = 0
        self.crct_questions = 0


        self.createWindow()
    
    def repeatFuntion(self):
        print('repeat is called man')
        self.repeatFlag = True
    
    def skipButtonFucntion(self):
        self.tutorialFlag=False
        self.letter_label.grid_forget()
        self.helper_label.grid_forget()
        self.skipButton.grid_forget()
    
    def nextFunction(self):
        self.nextButtonFlag = True
        if not self.threadLock.locked():
            self.threadLock.acquire()
   
            if self.change_label:
                self.change_label  = False
                self.instruction_counter+=1
                threading.Thread(target=self.instructionThread,args=(),daemon=True,).start()
            
            self.threadLock.release()


    
    
    def timerThread(self):
        print("Timer Thread: I am starting ")
        self.threadLock.acquire()
        self.time_complete_flag = False
        self.threadLock.release()
        time.sleep(TEST_DURATION)
        self.threadLock.acquire()
        self.time_complete_flag = True
        self.threadLock.release()
        print("Timer thread : I am dying")


    def createWindow(self):
        self.nextButton = tk.Button(self,text="Next",font=("Times",15,"normal"),relief="ridge",command=self.nextFunction,pady=2)
        self.nextButton.grid(row=5,column=1,)
        self.letter_label = tk.Label(self,text="",font=('Times',150,'normal'),bg="#3E8188",fg="white")
        self.helper_label =tk.Label(self,text="",font=('Times',20,'normal'),bg="#3E8188",fg="white")
        self.repeatBtn = tk.Button(self,text="Repeat",relief="ridge",font=("Times",15,"normal"),command=self.repeatFuntion,pady=2)
        self.skipButton = tk.Button(self,text="Skip the Tutorial",font=("Times",15,"normal"),relief='ridge',command=self.skipButtonFucntion,pady=2)
        im_1_1 = Image.open(BASE_DIR+"\\tinkerpro\\img\\wordusefluency.png")
        im_1_1 = im_1_1.resize((600,400),Image.ANTIALIAS)
        image_list_other.append(ImageTk.PhotoImage(im_1_1))
        self.image_label = tk.Label(self,
            image = image_list_other[0],
            bg="#3E8188",)
        self.image_label.grid(row=3,column=1,pady=5)
            

    def instructionThread(self):
        
        tag="Instruction Thread: "
        toggle_repeat= True
        print(self.helper_label.winfo_exists())
        print(tag+ "I am called "+str(self.instruction_counter))
        toggle =True
        count=1
        path=BASE_DIR+"\\tinkerpro\\recordwordusetest"
        if self.instruction_counter in [1,2,3,5]:
            self.instruction_label['text' ] = self.instruction_dict[self.instruction_counter]
            self.nextButton['state'] =tk.DISABLED
            myobj = gTTS(text=self.instruction_label['text'], lang=language, slow=False,) 
            myobj.save("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
            playsound("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
            os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
            self.RECORDINGCOUNT+=1
            self.nextButton['state'] = tk.NORMAL
        elif self.instruction_counter == 4:
            self.image_label.grid_forget()
            self.instruction_label['text'] = self.instruction_dict[self.instruction_counter]
            myobj = gTTS(text=self.instruction_label['text'], lang=language, slow=False,) 
            myobj.save("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
            playsound("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
            os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
            self.RECORDINGCOUNT+=1
            self.nextButton.grid_forget()
            self.skipButton.grid(row=5,column=1)
            self.helper_label.grid(row=2,column=1)
            self.letter_label['text'] = "Rabbit"
            self.letter_label.grid(row=3,column=1)
            threading.Thread(target=self.initRecognition,args=("rabbit"),daemon=True).start()
            while(True):
                self.threadLock.acquire()
                if (self.failed_flag and toggle ) or (self.failed_flag and self.repeatFlag):
                   
                    print(tag+"I am in failed flag")
                    self.failed_flag=False
                    self.instruction_label['text'] = "You didnt use the word ' Rabbit' i will repeat it again"
                    myobj = gTTS(text=self.instruction_label['text'], lang=language, slow=False,) 
                    myobj.save("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                    playsound("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                    os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                    self.RECORDINGCOUNT+=1
                    self.instruction_label['text'] =  self.instruction_dict[4]
                    
                    myobj = gTTS(text=self.instruction_label['text'], lang=language, slow=False,) 
                    myobj.save("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                    playsound("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                    os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                    self.RECORDINGCOUNT+=1
                    threading.Thread(target=self.initRecognition,args=("rabbit"),daemon=True).start()
                    count+=1
                    if count ==2:
                        toggle =False
                    self.completed_listening_flag = False
                    if self.repeatFlag:
                        self.repeatFlag=False
                        self.repeatBtn.grid_forget()
                        self.nextButton.grid(row=5,column=1)

                    
                    

                elif self.failed_flag and not toggle and self.completed_listening_flag  and toggle_repeat:
                    toggle_repeat=False
                    print(tag+"I am in another failed flag")
                    self.instruction_label['text']  = "If you want we can  repeat the tutorial"
                    myobj = gTTS(text=self.instruction_label['text'], lang=language, slow=False,) 
                    myobj.save("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                    playsound("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                    os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                    self.RECORDINGCOUNT+=1
                    self.repeatBtn.grid(row=5,column=2)
                    self.nextButton.grid(row=5,column=0)

                elif not self.tutorialFlag:
                    self.tutorialFlag=True
                    print(tag+"I am ending from exit ")
                    self.completed_listening_flag = False
                    self.failed_flag = False
                    self.nextButton.grid(row=5,column=1)
                    self.threadLock.release()
                    self.change_label=True
                    exit()   
                elif self.completed_listening_flag:
                    self.completed_listening_flag=False
                    self.failed_flag=False
                    self.threadLock.release()
                    self.skipButton.grid_forget()
                    self.helper_label.grid_forget()
                    self.letter_label.grid_forget()
                    self.nextButton.grid(row=5,column=1)
                    break

            
                self.threadLock.release()
            
        elif self.instruction_counter>5:
            self.nextButton.grid_forget()
            self.letter_label.grid(row=3,column=1)
            self.helper_label.grid(row=2,column=1)
            self.completed_listening_flag =True
                    
            count_temp=1
            threading.Thread(target=self.timerThread,args=(),daemon= True).start()
            while(True):
                self.threadLock.acquire()
                if self.time_complete_flag:
                    break
                self.threadLock.release()
                if self.completed_listening_flag:
                            self.completed_listening_flag=False 
                            self.helper_label['text']  = "Listen carefully"
                        
                            print(self.word_dict[count_temp])
                            self.instruction_label['text'] = "Use the word " +self.word_dict[count_temp]
                            self.letter_label['text']=self.word_dict[count_temp]
                            myobj = gTTS(text=self.instruction_label['text'], lang=language, slow=False,) 
                            myobj.save("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                            playsound("recordwordusetest"+str(self.RECORDINGCOUNT)+".mp3")
                            os.remove(path+str(self.RECORDINGCOUNT)+".mp3")
                            self.RECORDINGCOUNT+=1
                            self.total_questions +=1
                            threading.Thread(target=self.initRecognition,args=(self.word_dict[count_temp]),daemon=True).start()
                            count_temp+=1
            global totalquestions
            global crctquestions
            totalquestions =self.total_questions
            crctquestions = self.crct_questions
            self.app.append(self)
            self.app[0].switchFrame(evaluation.Evaluation,self.app[1:])
                                 
        self.change_label=True
 
        print(tag+"I am ending")

        

                



    def initRecognition(self,word,*args, **kwargs):
        tag='Init recognition'
        print("Init Recognition"+"I am called")
        recognised_flag=True
        r=sr.Recognizer()
        mic= sr.Microphone()
        print("speak")
        self.helper_label['text'] = "Speak I am Listening...."
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source,duration=0.8)
                audio = r.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                print("You didnt speak anything")
                self.failed_flag=True
                recognised_flag=False
                
        
        if recognised_flag:       
            self.helper_label['text']= "Processing....Be patient"
            try:
                recognisedPhrase= r.recognize_google(audio)
                print(recognisedPhrase)
                if word.lower() in recognisedPhrase.lower():
                    self.crct_questions+=1
                    print(True)
                else:
                    print(False)
                    
            except sr.UnknownValueError :
                self.helper_label['text']  = "You spoke incorrectly"
                time.sleep(4)
            except sr.URLError:
                messagebox.Message("No internet Connection check Your connection and restart the program")

        self.helper_label['text'] = "Almost Done !"   
        self.threadLock.acquire()
        self.completed_listening_flag = True
        self.threadLock.release()
        print("Init Recognition"+"I am ending"+word)        
            
        


    
    
            
        
        


        
        
        


        





        


