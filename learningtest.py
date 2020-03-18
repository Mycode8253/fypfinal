import  tkinter as tk
import tkinter.ttk as ttk 
from tkinter import messagebox
import string as st
import random
import time
import threading
import speech_recognition as sr

class LearningTest(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.lock = threading.Lock()
        #tk.Frame.configure(self,bg='blue')
        self.letters =   st.ascii_letters           # returns a list of asci letters from a to z and 'A' to 'Z' 
        self.letter_label = tk.Label(self,text="",font=('Calibre',150))
        self.instruction_label = tk.Label(self,text="Hey Hello!!",font=('Calibre',20))
        #master.geometry("500x200")                  # change geometry height and widht(height x width)
        self.progress_bar_determinate = ttk.Progressbar(self,orient=tk.HORIZONTAL,length=100, mode='determinate')
        self.progress_bar_indeterminate = ttk.Progressbar(self,orient=tk.HORIZONTAL,length=100, mode='indeterminate')
        self.start_button = tk.Button(self,text="Start the Test",command= self.startThread)
        self.process_running_label = tk.Label(self,text="",font=('Calibre',20))
        self.start  = False
        self.complete_flag = True
        self.createWindow()
        threading.Thread(target=self.instructionThread,args=(),daemon=True).start()


    def createRandomNumber(self):
      random_letter =  random.choice(self.letters)  # generates a random letter from the given list of letters
      return random_letter


    def createWindow(self):
        tk.Label(self,text="Learning Fluency Test",font=('Calibre',20)).grid(row=0,column=2,ipady=2,ipadx=2,sticky=tk.N)
      
        self.instruction_label.grid(row=1,column=2,pady=2)
        self.letter_label.grid(row=2,column=2,pady=2)
        self.progress_bar_determinate.grid(row=4,column=2)
        
        
        
    def barThread(self,value,complete_flag):
      if  value!=100 or (not complete_flag):
        self.progress_bar_determinate['value']= value
        self.update_idletasks()
      else:
        print("i am removed###########")
        self.progress_bar_determinate.grid_forget()
        

    def startThread(self):
      tag="startThread:"
      print(tag+"I am called")
      self.start = True


    def timer(self):
      bar_level=10
      print("timer is called")
      while(True):
        #self.lock.acquire()
        if self.complete_flag:
          self.barThread(100,False)
          self.complete_flag  =False
         # self.lock.release()
          break
        else:
          self.barThread(bar_level+10,False)
          #self.lock.release()
          time.sleep(5)  
    
      
    def instructionThread(self,*awrgs,**kwargs):
      tag = "instructionThread:"
      print(tag +" i am called ")

      self.instruction_label['text']="You will be given a set of letters \n you have to speak out louder\n letter will stay for a period of time and it will disappear you should tell it when it disappears\n we will start when you are ready :-)"
      self.start_button.grid(row=3,column=2,pady=2)
      self.process_running_label.grid(row=4,column=2)
      while(True):
        if self.start:
          self.start_button.grid_forget()
          self.progress_bar_determinate.grid(row=5,column=2,pady=2)
          self.barThread(0,False)
          break
        
      self.instruction_label['text'] = "Here they come"
      count=0
      while(True):
        thread = threading.Thread(target=self.initRecognition,args=(self.createRandomNumber()),daemon=True)
        self.lock.acquire()
        if  (not thread.isAlive() )and (self.complete_flag) :
          self.complete_flag= False
          self.lock.release()
          if count <10:
            count+=1
            
            thread.start()
          else:
            break
        else:
          self.lock.release()
      self.process_running_label.grid_forget()
      self.instruction_label['text'] = "done with the test"
    
      print(tag+"i am going down")





    def initRecognition(self,word,*args,**kwargs):
        self.letter_label['text'] = word
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
          if recognisedPhrase == word.lower():
              print(True)
          else:
              print(False)
          
        except sr.UnknownValueError:
            messagebox.showinfo('Message',"What you spoke didnt make any sense try one more time ")
        finally:
          self.barThread(80,False)
          self.process_running_label['text'] = "Almost Done !"
          self.lock.acquire()
          self.complete_flag = True
          self.lock.release()
          self.barThread(100,False)
        

      
      







       
      
   # def instructionMethod(self):


        
        
