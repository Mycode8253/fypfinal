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
        self.letters =   st.ascii_letters           # returns a list of asci letters from a to z or 'A' to 'Z' 
        self.letter_label = tk.Label(self,text="",font=('Calibre',150))
        self.instruction_label = tk.Label(self,text="Hey Hello!!",font=('Calibre',20))
        #master.geometry("500x200")                  # change geometry height and widht(height x width)
        self.progress_bar_determinate = ttk.Progressbar(self,orient=tk.HORIZONTAL,length=100, mode='determinate')
        self.progress_bar_indeterminate = ttk.Progressbar(self,orient=tk.HORIZONTAL,length=100, mode='indeterminate')
        self.start_button = tk.Button(self,text="Start the Test",command= self.startThread)
        self.process_running_label = tk.Label(self,text="",font=('Calibre',20))
        self.start  = False
        self.repeat =False
        self.complete_flag = True
        self.next_flag = True
        self.total_letter_counter = 0
        self.crct_letter_counter=0
        self.repeat_Btn = tk.Button(self,text="Repeat the instruction",command=self.repeatFunc,)
        self.createWindow()
        self.done_Timer_Flag = False
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
      self.next_flag=True
    


    def repeatFunc(self):
      self.repeat=True



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

    def timerThread(self,*awrgs,**kwargs):
      tag="TimerThread"
      print(tag+ " I am called")
      time_interval = 60
      self.lock.acquire()
      self.done_Timer_Flag = False
      self.lock.release()
      time.sleep(time_interval)
      self.lock.acquire()
      self.done_Timer_Flag = True
      self.lock.release()
      print(tag+"I am ending master test should also end ......")


    def instructionThread(self,*awrgs,**kwargs):
      tag = "instructionThread:"
      print(tag +" i am called ")
      instruction_word_dic = {
          1:"Welcome to the test..",
          2:"Here are the instructions to follow it out",
          3:"Here are some letters that keeps on coming in this fashion",
          4:"You should be telling it loud, what is that letter ",
          5:"You will be given 5 seconds to speak out the letter",
          6:"it keeps on going like that \n if you want to repeat again the instructions click on repeat again \n if not lets start!",

      }
      temp_int_counter =1
      self.repeat=False
      self.start_button.grid(row=3,column=2,pady=2)

      while(True):
        if self.next_flag and temp_int_counter<=6:
          self.instruction_label['text'] = instruction_word_dic[temp_int_counter]
          self.start_button['text']='Next ->'
          self.next_flag=False
          if(temp_int_counter==6):
            self.start_button['text'] = "Start!"
            self.repeat_Btn.grid(row=4,column=2,pady=2)

          temp_int_counter +=1
        
        elif self.repeat:
          self.repeat_Btn.grid_forget()
          self.repeat=False
          temp_int_counter=2
          self.next_flag=True
        
        elif self.next_flag and temp_int_counter>6:
          self.repeat_Btn.grid_forget()
          break

      self.process_running_label.grid(row=4,column=2)
      while(True):
        if self.start:
          self.start_button.grid_forget()
          self.progress_bar_determinate.grid(row=5,column=2,pady=2)
          self.barThread(0,False)
          break
        
      self.instruction_label['text'] = "Here they come"
      count=False
      threading.Thread(target=self.timerThread,args=(),daemon=True).start()
      while(True):
        thread = threading.Thread(target=self.initRecognition,args=(self.createRandomNumber()),daemon=True)
        self.lock.acquire()
        if  (not thread.isAlive()) and (self.complete_flag) :
          self.complete_flag= False
          count  = self.done_Timer_Flag
          self.lock.release()
          if not count:
            self.total_letter_counter+=1
            thread.start()
          else:
            break
        else:
          self.lock.release()
      self.process_running_label.grid_forget()
      self.instruction_label['text'] = "done with the test"
      print(tag+"I am going down")
      print(tag+"Total asked : "+str(self.total_letter_counter)+"crct words: "+str (self.crct_letter_counter))





    def initRecognition(self,word,*args,**kwargs):
        print("I am called for this: "+ word)
        trail_counter = 1
        self.letter_label['text'] = word
        r=sr.Recognizer()
        mic= sr.Microphone()
        print("speak")
        self.barThread(20,False)
        self.process_running_label['text'] = "Speak I am Listening...."
        with mic as source:
            try:              
                r.adjust_for_ambient_noise(source,duration=  0.1)
                audio = r.listen(source, timeout=5,)
                self.barThread(50,False)
                
            except sr.WaitTimeoutError:
                #messagebox.showinfo('Message',"You didnt speak anything please speak again")
                self.instruction_label['text'] = "You didnt speak anything please speak again" #instead of the instruction label you should be getting the voice overs made by priya or someone 
                if trail_counter!=2:
                  threading.Thread(target=self.initRecognition,args=(word),daemon=True).start()
                  exit()





        try:
          self.process_running_label['text'] = "Processing....Be patient"
          recognisedPhrase= r.recognize_google(audio)
          print(recognisedPhrase)
          if recognisedPhrase == word.lower():
              print(True)
              self.crct_letter_counter+=1
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
        

      
      










        
        
