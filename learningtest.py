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
        self.start_button = tk.Button(self,text="Start the Test",command= lambda: self.startThread())
        self.start  = False
        self.createWindow()
        threading.Thread(target=self.instructionThread,args=(),daemon=True).start()


  
        

    def createRandomNumber(self):
      random_letter =  random.choice(self.letters)  # generates a random letter from the given list of letters
      self.letter_label['text'] = random_letter
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
      print("timer is called")
      self.barThread(30,False)
      time.sleep(10)
      self.barThread(60,False)
      time.sleep(5)
      self.barThread(90,False)
      time.sleep(5)
      self.barThread(100,False)







    def instructionThread(self,*awrgs,**kwargs):
      tag = "instructionThread:"
      print(tag +" i am called ")
     
    
      self.instruction_label['text']="You will be given a set of letters \n you have to speak out louder\n letter will stay for a period of time and it will disappear you should tell it when it disappears\n we will start when you are ready :-)"
      self.start_button.grid(row=3,column=2,pady=2)

      while(True):
        if self.start:
          self.start_button.grid_forget()
          self.progress_bar_determinate.grid(row=4,column=2,pady=2)
          self.barThread(0,False)
          self.timer()
          break
        
      self.instruction_label['text'] = "Here they come"
      count=0
      while(True):
        thread = threading.Thread(target=self.initRecognition,args=(self.createRandomNumber()),daemon=True)
        if not thread.isAlive():
          if count <10:
            count+=1
            thread.start()
            self.timer()  
          else:
            break
        
        
      




     

      self.instruction_label['text'] = "done with the test"
        


      





      print(tag+"i am going down")





    def initRecognition(self,word,*args,**kwargs):
        r=sr.Recognizer()
        mic= sr.Microphone()
        print("speak")
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source,duration=  1)
                audio = r.listen(source, phrase_time_limit=10)
                
            except sr.WaitTimeoutError:
                messagebox.showinfo('Message',"You didnt speak anything please speak again")
        
                
        try:
            recognisedPhrase= r.recognize_google(audio)
            print(recognisedPhrase)
            if recognisedPhrase == word.lower():
                print(True)
            else:
                print(False)
        except sr.UnknownValueError:
            messagebox.showinfo('Message',"What you spoke didnt make any sense try one more time ")

      
      







       
      
   # def instructionMethod(self):


        
        