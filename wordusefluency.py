import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
import speech_recognition as sr
import time


TEST_DURATION=2




class WordUseFluency(tk.Frame):

    def __init__(self,master,*args,**kawrgs):
        print(args)
        tk.Frame.__init__(self,master)
        tk.Label(self, font=('Times',24,'normal'), text="Word Use Fluency Test",).grid(row=0, column=1)
        self.instruction_label = tk.Label(self, font=('Times', '20', 'normal'), text="Hey Hello! you came so far...",)
        self.instruction_label.grid(row=1,column=1,pady=5)
        self.helper_label = None
        #Helpfull variables
        self.instruction_dict = {
            1:"Hey welcome to the test ",
            2:"Listen to me using this word 'Green' The grass is green ",
            3:"Here is another word 'jump' I would like to jump ",
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
        }
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


        self.createWindow()
    
    def repeatFuntion(self):
        print('repeat is called man')
        self.repeatFlag = True
    
    def skipButtonFucntion(self):
        self.tutorialFlag=False
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
        self.nextButton = tk.Button(self,text="Next",relief="ridge",command=self.nextFunction)
        self.nextButton.grid(row=5,column=1,)
        self.word_label = tk.Label(self,text="",)
        self.letter_label = tk.Label(self,text="",font=('Times',150,'normal'),bg="#120E4A",fg='white')
        self.helper_label =tk.Label(self,text="",font=('Times',20,'normal'),bg="#120E4A",fg='white')
        self.repeatBtn = tk.Button(self,text="Repeat",relief="ridge",command=self.repeatFuntion)
        self.skipButton = tk.Button(self,text="Skip the Tutorial",relief='ridge',command=self.skipButtonFucntion)

    def instructionThread(self):
        tag="Instruction Thread: "
        toggle_repeat= True
        print(self.helper_label.winfo_exists())
        print(tag+ "I am called "+str(self.instruction_counter))
        toggle =True
        count=1
        if self.instruction_counter in [1,2,3,5]:
            self.instruction_label['text' ] = self.instruction_dict[self.instruction_counter]
        elif self.instruction_counter == 4:
            self.instruction_label['text'] = self.instruction_dict[self.instruction_counter]
            self.nextButton.grid_forget()
            self.skipButton.grid(row=5,column=1)
            threading.Thread(target=self.initRecognition,args=("rabbit"),daemon=True).start()
            while(True):
                self.threadLock.acquire()
                if (self.failed_flag and toggle ) or (self.failed_flag and self.repeatFlag):
                   
                    print(tag+"I am in failed flag")
                    self.failed_flag=False
                    self.instruction_label['text'] = "You didnt use the word ' Rabbit' i will repeat it again"
                    time.sleep(5)
                    self.instruction_label['text'] =  self.instruction_dict[4]
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
                    break

            
                self.threadLock.release()
            
        elif self.instruction_counter>5:
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
                            threading.Thread(target=self.initRecognition,args=(self.word_dict[count_temp]),daemon=True).start()
                            print(self.word_dict[count_temp])
                            self.instruction_label['text'] = "Use the word" +self.word_dict[count_temp]
                            self.letter_label['text']=self.word_dict[count_temp]
                            count_temp+=1
                                 
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
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                print("You didnt speak anything")
                self.failed_flag=True
                recognised_flag=False
                
        
        if recognised_flag:       
            self.helper_label['text']= "Processing....Be patient"
            try:
                recognisedPhrase= r.recognize_google(audio)
                if word.lower() in recognisedPhrase.lower():
                    print(True)
                else:
                    print(False)
                    
            except sr.UnknownValueError:
                messagebox.showinfo('Message',"What you spoke didnt make any sense try one more time ")

        self.helper_label['text'] = "Almost Done !"   
        self.threadLock.acquire()
        self.completed_listening_flag = True
        self.threadLock.release()
        print("Init Recognition"+"I am ending"+word)        
            
        


    
    
            
        
        


        
        
        


        





        


