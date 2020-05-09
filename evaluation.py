
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

        # Dont touch this  
        ######################################Sensitive code if one thing is changed then the whole thing has to be rewritten 
        temp1 = awrgs[1]
        for item1 in temp1:
            print(item1)
     
        self.worduseclass = item1[1]
        temp1= item1[0]
        temp2=temp1[0]
        self.learningtest = temp2[1]
        self.imagetest = temp2[0]
        self.imagetest = self.imagetest[0]
        #####################################
    
    
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
            
        temp1=self.imagetest.crct_answered/self.imagetest.total_questions
        temp2= self.learningtest.crct_letter_counter/self.learningtest.total_letter_counter
        temp3= self.worduseclass.crct_questions/self.worduseclass.total_questions

        if temp1 >2 and temp2 >2 and temp3 >2:
            Label2['text'] = "No risk at all"
        elif (temp1>2 and temp2<2 and temp3 >2) or (temp1>2 and temp2 >2 and temp3<2):
            Label2['text'] = " No risk at all but do refer in future"
        elif (temp1<2 and temp2>2 and temp3 >2):
            Label2['text'] = "Medium risk take the test one more time"
        elif (temp1<2 and temp2<2 and temp3 >2) or (temp1>2 and temp2 <2 and temp3 < 2):
            Label2['text'] = "Medium risk"
        elif temp1<2 and temp2<2 and temp3 <2:
            Label2['text'] = "At risk"
            
        
   

        Label2['text'] = "Initial Fluency Test"+str(self.imagetest.crct_answered/self.imagetest.total_questions) 
        Label3 = tk.Label(self, font=('Times',24,'normal'), text="Game",bg = '#EA696B',fg='#FCF7D9')
        Label3.grid(
            row=4, column=1,pady=2)
        Label3['text'] = "Letter learning Fluency" + str(self.learningtest.crct_letter_counter/self.learningtest.total_letter_counter)

        Label4 = tk.Label(self, font=('Times',24,'normal'), text="Game",bg = '#EA696B',fg='#FCF7D9')
        Label4.grid(row=5, column=1,pady=2)
        Label4['text'] = "Word Use Fluency Test" + str(self.worduseclass.crct_questions/self.worduseclass.total_questions)
        print("I am ending people")




        

    





        print(Image_test_Dyslexia.imageCorrectAnswers)
