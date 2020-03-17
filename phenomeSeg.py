import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
import speech_recognition as sr






class PhenomeSegmentation(tk.Frame):

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        # Thread variables

        self.wordqueue = []
        self.lockstatus = threading.Lock()

        # Thread variables
        self.question_label = tk.Label(self,text="Question?",font=('Calibre',30))
        self.progress_bar_determinate = ttk.Progressbar(self,orient=tk.HORIZONTAL,length=100, mode='determinate')
        self.mbutton = tk.Button(self,text='Lets start!!',command = threading.Thread(target=self.instructionThread,args=(),daemon=True).start)
        self.slash_text  = tk.Label(self,text="/Qu/es/tion",font=('Calibre',20))
        self.process_running_label = tk.Label(self,text="",font=('Calibre',20))
        self.complete_flag =False
        self.createWindow()
        


    def createWindow(self):
        self.question_label.grid(row = 0,column = 1)
        self.slash_text.grid(row = 1,column = 1)
        self.question_label['text'] = "Hey, lets begin the test when you are ready :-)"
        self.mbutton.grid(row=2,column=1)
        threading.Thread(target=self.initRecognition,args=(),daemon=True).start
        
    def barThread(self,value,complete_flag):
      if  value!=100 or (not complete_flag):
        self.progress_bar_determinate['value']= value
        self.update_idletasks()
      else:
        print("i am removed###########")
        self.progress_bar_determinate.grid_forget()    

    
    def initRecognition(self,*args,**kwargs):
        print("I am called ")
        while( True ):
            if((len(self.wordqueue)!=0 )):
                r=sr.Recognizer()
                mic= sr.Microphone()
                print("speak")
                self.barThread(20,False)
                self.process_running_label['text'] = "Speak I am Listening...."
                with mic as source:
                    try:              
                        r.adjust_for_ambient_noise(source,duration=  0.1)
                        audio = r.listen(source, timeout=20,)
                        self.barThread(50,False)
                        
                    except sr.WaitTimeoutError:
                        messagebox.showinfo('Message',"You didnt speak anything please speak again")
                try:
                    self.process_running_label['text'] = "Processing....Be patient"
                    recognisedPhrase= r.recognize_google(audio)
                    print(recognisedPhrase)
                    '''
                    if recognisedPhrase == word.lower():
                        print(True)
                    else:
                        print(False)
                    '''
                
                except sr.UnknownValueError:
                    messagebox.showinfo('Message',"What you spoke didnt make any sense try one more time ")
                finally:
                    self.barThread(80,False)
                    self.process_running_label['text'] = "Almost Done !"
                    self.lockstatus.acquire()
                    self.complete_flag = True
                    print(len(self.wordqueue)-1)
                    self.wordqueue.pop(len(self.wordqueue)-1)
                    self.lockstatus.release()
                    self.barThread(100,False)
                    
            elif self.complete_flag:
                print("i am out ")
                break
            
        


    def instructionThread(self):
        self.mbutton.grid_forget()
        self.process_running_label.grid(row=3,column =1)
        self.progress_bar_determinate.grid(row=4,column=1)
        self.question_label['text'] = "Split the word \"Happy\" "
        self.slash_text['text'] = "\\Ha \\ppy"
        self.lockstatus.acquire()
        self.wordqueue.append("Ha")
        threading.Thread(target=self.initRecognition,args=(),daemon=True).start()
        self.complete_flag  = True
        self.lockstatus.release()


        
        





        


