
import tkinter as tk
import tkinter.ttk as ttk
import Image_test_Dyslexia
import learningtest
TEST_DURATION = 3   #seconds genarally 3 minutes 
SIZE = (250, 250)
PADDING_IMAGE_X = 10
PADDING_IMAGE_Y = 10

image_list = []
image_list_other= []
image_list_second=[]

class Evaluation(tk.Frame):
    def __init__(self, master,*awrgs,**kwargs):
        tk.Frame.__init__(self, master,bg = '#3E8188')
   
        self.Question = tk.Label(self, font=('Times', '20', 'normal'), text="",bg = '#3E8188')
        tk.Label(self, font=('Times',24,'normal'), text="Evaluation",bg = '#3D8188').grid(
            row=0, column=1)
        self.app = awrgs[0]
        self.app.configure(background="#3D8188")
        self.Question.grid(row=1,column=1,pady=2)
        self.Question["text"]="No one cares what prints here coz it's over"

        print(Image_test_Dyslexia.imageCorrectAnswers)
